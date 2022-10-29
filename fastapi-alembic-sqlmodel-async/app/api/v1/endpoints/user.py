from io import BytesIO
from typing import Optional
from uuid import UUID

from app import crud
from app.api import deps
from app.models import User, UserFollow
from app.models.role_model import Role
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
from app.utils.minio_client import MinioClient
from app.utils.resize_image import modify_image
from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    HTTPException,
    Query,
    Response,
    UploadFile,
    status,
)
from fastapi_pagination import Params
from sqlmodel import and_, select

router = APIRouter()


@router.get("/list", response_model=IGetResponsePaginated[IUserReadWithoutGroups])
async def read_users_list(
    params: Params = Depends(),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    """
    Retrieve users. Requires admin or manager role
    """
    users = await crud.user.get_multi_paginated(params=params)
    return create_response(data=users)


@router.get(
    "/list/by_role_name",
    response_model=IGetResponsePaginated[IUserReadWithoutGroups],
)
async def read_users_list_by_role_name(
    user_status: Optional[IUserStatus] = Query(
        default=IUserStatus.active,
        description="User status, It is optional. Default is active",
    ),
    role_name: str = Query(
        default="", description="String compare with name or last name"
    ),
    params: Params = Depends(),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
):
    """
    Retrieve users by role name and status. Requires admin role
    """
    user_status = True if user_status == IUserStatus.active else False
    role = await crud.role.get_role_by_name(name=role_name)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role name is invalid")
    query = (
        select(User)
        .join(Role, User.role_id == Role.id)
        .where(and_(Role.name == role_name, User.is_active == user_status))
        .order_by(User.first_name)
    )
    users = await crud.user.get_multi_paginated(query=query, params=params)
    return create_response(data=users)


@router.get(
    "/order_by_created_at",
    response_model=IGetResponsePaginated[IUserReadWithoutGroups],
)
async def get_hero_list_order_by_created_at(
    params: Params = Depends(),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    """
    Gets a paginated list of users ordered by created datetime
    """
    query = select(User).order_by(User.created_at)
    users = await crud.user.get_multi_paginated(query=query, params=params)
    return create_response(data=users)


@router.get("/following", response_model=IGetResponsePaginated[IUserFollowReadCommon])
async def get_following(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
):
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
            UserFollow.is_mutual
        )
        .join(UserFollow, User.id == UserFollow.target_user_id)
        .where(UserFollow.user_id == current_user.id)
    )
    users = await crud.user.get_multi_paginated(query=query, params=params)
    return create_response(data=users)


@router.get("/followers", response_model=IGetResponsePaginated[IUserFollowReadCommon])
async def get_followers(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
):
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
            UserFollow.is_mutual
        )
        .join(UserFollow, User.id == UserFollow.user_id)
        .where(UserFollow.target_user_id == current_user.id)
    )
    users = await crud.user.get_multi_paginated(query=query, params=params)
    return create_response(data=users)


@router.put("/following/{target_user_id}", response_model=IPutResponseBase[IUserFollowRead])
async def follow_a_user_by_id(
    target_user_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Following a user
    """
    target_user = await crud.user.get(id=target_user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User id is invalid")

    current_follow_user = (
        await crud.user_follow.get_follow_by_user_id_and_target_user_id(
            user_id=current_user.id, target_user_id=target_user_id
        )
    )
    if current_follow_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This user has been followed"
        )

    new_user_follow = await crud.user_follow.follow_a_user_by_target_user_id(
        user=current_user, target_user=target_user
    )
    return create_response(data=new_user_follow)


@router.delete("/following/{target_user_id}", response_model=IDeleteResponseBase[IUserFollowRead])
async def unfollowing_a_user_by_id(
    target_user_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Unfollowing a user
    """
    target_user = await crud.user.get(id=target_user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User id is invalid")

    current_follow_user = await crud.user_follow.get_follow_by_target_user_id(
        user_id=current_user.id, target_user_id=target_user_id
    )

    if not current_follow_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user has not been followed")

    user_follow = await crud.user_follow.unfollow_a_user_by_id(
        user_follow_id=current_follow_user.id,
        user=current_user,
        target_user=target_user,
    )
    return create_response(data=user_follow)


@router.get("/{user_id}", response_model=IGetResponseBase[IUserRead])
async def get_user_by_id(
    user_id: UUID,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    """
    Gets a user by his/her id
    """
    user = await crud.user.get(id=user_id)
    if user:
        return create_response(data=user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User id is invalid")


@router.get("", response_model=IGetResponseBase[IUserRead])
async def get_my_data(
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Gets my user profile information
    """
    return create_response(data=current_user)


@router.post("", response_model=IPostResponseBase[IUserRead], status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: IUserCreate = Depends(deps.user_exists),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
):
    """
    Creates a new user
    """

    role = await crud.role.get(id=new_user.role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role id is invalid")

    user = await crud.user.create_with_role(obj_in=new_user)
    return create_response(data=user)


@router.delete("/{user_id}", response_model=IDeleteResponseBase[IUserRead])
async def remove_user(
    user: User = Depends(deps.is_valid_user),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
):
    """
    Deletes a user by his/her id
    """
    if current_user.id == user.id:
        raise HTTPException(status_code=404, detail="Users can not delete theirselfs")

    user = await crud.user.remove(id=user.id)
    return create_response(data=user)


@router.post("/image", response_model=IPostResponseBase[IUserRead])
async def upload_my_image(
    title: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    image_file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user()),
    minio_client: MinioClient = Depends(deps.minio_auth),
):
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


@router.post("/{user_id}/image", response_model=IPostResponseBase[IUserRead])
async def upload_user_image(
    user: User = Depends(deps.is_valid_user),
    title: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    image_file: UploadFile = File(...),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
    minio_client: MinioClient = Depends(deps.minio_auth),
):
    """
    Uploads a user image by his/her id
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
