from io import BytesIO
from typing import Annotated
from uuid import UUID
from app.utils.exceptions import (
    IdNotFoundException,
    SelfFollowedException,
    UserFollowedException,
    UserNotFollowedException,
    UserSelfDeleteException,
)
from app import crud
from app.api import deps
from app.deps import user_deps
from app.models import User, UserFollow
from app.models.role_model import Role
from app.utils.minio_client import MinioClient
from app.utils.resize_image import modify_image
from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Query,
    Response,
    UploadFile,
    status,
)
from app.schemas.media_schema import IMediaCreate
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleEnum
from app.schemas.user_follow_schema import IUserFollowRead
from app.schemas.user_schema import (
    IUserCreate,
    IUserRead,
    IUserReadWithoutGroups,
    IUserStatus,
)
from app.schemas.user_follow_schema import (
    IUserFollowReadCommon,
)
from fastapi_pagination import Params
from sqlmodel import and_, select, col, or_, text

router = APIRouter()


@router.get("/list")
async def read_users_list(
    params: Params = Depends(),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IGetResponsePaginated[IUserReadWithoutGroups]:
    """
    Retrieve users. Requires admin or manager role

    Required roles:
    - admin
    - manager
    """
    users = await crud.user.get_multi_paginated(params=params)
    return create_response(data=users)


@router.get("/list/by_role_name")
async def read_users_list_by_role_name(
    name: str = "",
    user_status: Annotated[
        IUserStatus,
        Query(
            title="User status",
            description="User status, It is optional. Default is active",
        ),
    ] = IUserStatus.active,
    role_name: str = "",
    params: Params = Depends(),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
) -> IGetResponsePaginated[IUserReadWithoutGroups]:
    """
    Retrieve users by role name and status. Requires admin role

    Required roles:
    - admin
    """
    user_status = True if user_status == IUserStatus.active else False
    query = (
        select(User)
        .join(Role, User.role_id == Role.id)
        .where(
            and_(
                col(Role.name).ilike(f"%{role_name}%"),
                User.is_active == user_status,
                or_(
                    col(User.first_name).ilike(f"%{name}%"),
                    col(User.last_name).ilike(f"%{name}%"),
                    text(
                        f"""'{name}' % concat("User".last_name, ' ', "User".first_name)"""
                    ),
                    text(
                        f"""'{name}' % concat("User".first_name, ' ', "User".last_name)"""
                    ),
                ),
            )
        )
        .order_by(User.first_name)
    )
    users = await crud.user.get_multi_paginated(query=query, params=params)
    return create_response(data=users)


@router.get("/order_by_created_at")
async def get_user_list_order_by_created_at(
    params: Params = Depends(),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IGetResponsePaginated[IUserReadWithoutGroups]:
    """
    Gets a paginated list of users ordered by created datetime

    Required roles:
    - admin
    - manager
    """
    users = await crud.user.get_multi_paginated_ordered(
        params=params, order_by="created_at"
    )
    return create_response(data=users)


@router.get("/following")
async def get_following(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IUserFollowReadCommon]:
    """
    Lists the people who the authenticated user follows.
    """
    query = (
        select(
            User.id,
            User.first_name,
            User.last_name,
            User.follower_count,
            User.following_count,
            UserFollow.is_mutual,
        )
        .join(UserFollow, User.id == UserFollow.target_user_id)
        .where(UserFollow.user_id == current_user.id)
    )
    users = await crud.user.get_multi_paginated(query=query, params=params)
    return create_response(data=users)


@router.get(
    "/following/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def check_is_followed_by_user_id(
    user: User = Depends(user_deps.is_valid_user),
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Check if a person is followed by the authenticated user
    """
    result = await crud.user_follow.get_follow_by_user_id_and_target_user_id(
        user_id=user.id, target_user_id=current_user.id
    )
    if not result:
        raise UserNotFollowedException(user_name=user.last_name)

    raise UserFollowedException(target_user_name=user.last_name)


@router.get("/followers")
async def get_followers(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IUserFollowReadCommon]:
    """
    Lists the people following the authenticated user.
    """
    query = (
        select(
            User.id,
            User.first_name,
            User.last_name,
            User.follower_count,
            User.following_count,
            UserFollow.is_mutual,
        )
        .join(UserFollow, User.id == UserFollow.user_id)
        .where(UserFollow.target_user_id == current_user.id)
    )
    users = await crud.user.get_multi_paginated(params=params, query=query)
    return create_response(data=users)


@router.get("/{user_id}/followers")
async def get_user_followed_by_user_id(
    user_id: UUID = Depends(user_deps.is_valid_user_id),
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IUserFollowReadCommon]:
    """
    Lists the people following the specified user.
    """
    query = (
        select(
            User.id,
            User.first_name,
            User.last_name,
            User.follower_count,
            User.following_count,
            UserFollow.is_mutual,
        )
        .join(UserFollow, User.id == UserFollow.user_id)
        .where(UserFollow.target_user_id == user_id)
    )
    users = await crud.user.get_multi_paginated(params=params, query=query)
    return create_response(data=users)


@router.get("/{user_id}/following")
async def get_user_following_by_user_id(
    user_id: UUID = Depends(user_deps.is_valid_user_id),
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IUserFollowReadCommon]:
    """
    Lists the people who the specified user follows.
    """
    query = (
        select(
            User.id,
            User.first_name,
            User.last_name,
            User.follower_count,
            User.following_count,
            UserFollow.is_mutual,
        )
        .join(UserFollow, User.id == UserFollow.target_user_id)
        .where(UserFollow.user_id == user_id)
    )
    users = await crud.user.get_multi_paginated(query=query, params=params)
    return create_response(data=users)


@router.get(
    "/{user_id}/following/{target_user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def check_a_user_is_followed_another_user_by_id(
    user_id: UUID,
    target_user_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Check if a user follows another user
    """
    if user_id == target_user_id:
        raise SelfFollowedException()

    user = await crud.user.get(id=user_id)
    if not user:
        raise IdNotFoundException(User, id=user_id)

    target_user = await crud.user.get(id=target_user_id)
    if not target_user:
        raise IdNotFoundException(User, id=target_user_id)

    result = await crud.user_follow.get_follow_by_user_id_and_target_user_id(
        user_id=user_id, target_user_id=target_user_id
    )
    if not result:
        raise UserNotFollowedException(
            user_name=user.last_name, target_user_name=target_user.last_name
        )


@router.put("/following/{target_user_id}")
async def follow_a_user_by_id(
    target_user_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IPutResponseBase[IUserFollowRead]:
    """
    Following a user
    """
    if target_user_id == current_user.id:
        raise SelfFollowedException()
    target_user = await crud.user.get(id=target_user_id)
    if not target_user:
        raise IdNotFoundException(User, id=target_user_id)

    current_follow_user = (
        await crud.user_follow.get_follow_by_user_id_and_target_user_id(
            user_id=current_user.id, target_user_id=target_user_id
        )
    )
    if current_follow_user:
        raise UserFollowedException(target_user_name=target_user.last_name)

    new_user_follow = await crud.user_follow.follow_a_user_by_target_user_id(
        user=current_user, target_user=target_user
    )
    return create_response(data=new_user_follow)


@router.delete("/following/{target_user_id}")
async def unfollowing_a_user_by_id(
    target_user_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IDeleteResponseBase[IUserFollowRead]:
    """
    Unfollowing a user
    """
    if target_user_id == current_user.id:
        raise SelfFollowedException()
    target_user = await crud.user.get(id=target_user_id)
    if not target_user:
        raise IdNotFoundException(User, id=target_user_id)

    current_follow_user = await crud.user_follow.get_follow_by_target_user_id(
        user_id=current_user.id, target_user_id=target_user_id
    )

    if not current_follow_user:
        raise UserNotFollowedException(user_name=target_user.last_name)

    user_follow = await crud.user_follow.unfollow_a_user_by_id(
        user_follow_id=current_follow_user.id,
        user=current_user,
        target_user=target_user,
    )
    return create_response(data=user_follow)


@router.get("/{user_id}")
async def get_user_by_id(
    user: User = Depends(user_deps.is_valid_user),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IGetResponseBase[IUserRead]:
    """
    Gets a user by his/her id

    Required roles:
    - admin
    - manager
    """
    return create_response(data=user)


@router.get("")
async def get_my_data(
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IUserRead]:
    """
    Gets my user profile information
    """
    return create_response(data=current_user)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: IUserCreate = Depends(user_deps.user_exists),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
) -> IPostResponseBase[IUserRead]:
    """
    Creates a new user

    Required roles:
    - admin
    """
    user = await crud.user.create_with_role(obj_in=new_user)
    return create_response(data=user)


@router.delete("/{user_id}")
async def remove_user(
    user_id: UUID = Depends(user_deps.is_valid_user_id),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
) -> IDeleteResponseBase[IUserRead]:
    """
    Deletes a user by his/her id

    Required roles:
    - admin
    """
    if current_user.id == user_id:
        raise UserSelfDeleteException()

    user = await crud.user.remove(id=user_id)
    return create_response(data=user, message="User removed")


@router.post("/image")
async def upload_my_image(
    title: str | None = Body(None),
    description: str | None = Body(None),
    image_file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user()),
    minio_client: MinioClient = Depends(deps.minio_auth),
) -> IPostResponseBase[IUserRead]:
    """
    Uploads a user image
    """
    try:
        image_modified = modify_image(BytesIO(image_file.file.read()))
        data_file = minio_client.put_object(
            file_name=image_file.filename,
            file_data=BytesIO(image_modified.file_data),
            content_type=image_file.content_type,
        )
        media = IMediaCreate(
            title=title, description=description, path=data_file.file_name
        )
        user = await crud.user.update_photo(
            user=current_user,
            image=media,
            heigth=image_modified.height,
            width=image_modified.width,
            file_format=image_modified.file_format,
        )
        return create_response(data=user)
    except Exception as e:
        print(e)
        return Response("Internal server error", status_code=500)


@router.post("/{user_id}/image")
async def upload_user_image(
    user: User = Depends(user_deps.is_valid_user),
    title: str | None = Body(None),
    description: str | None = Body(None),
    image_file: UploadFile = File(...),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
    minio_client: MinioClient = Depends(deps.minio_auth),
) -> IPostResponseBase[IUserRead]:
    """
    Uploads a user image by his/her id

    Required roles:
    - admin
    """
    try:
        image_modified = modify_image(BytesIO(image_file.file.read()))
        data_file = minio_client.put_object(
            file_name=image_file.filename,
            file_data=BytesIO(image_modified.file_data),
            content_type=image_file.content_type,
        )
        media = IMediaCreate(
            title=title, description=description, path=data_file.file_name
        )
        user = await crud.user.update_photo(
            user=user,
            image=media,
            heigth=image_modified.height,
            width=image_modified.width,
            file_format=image_modified.file_format,
        )
        return create_response(data=user)
    except Exception as e:
        print(e)
        return Response("Internal server error", status_code=500)
