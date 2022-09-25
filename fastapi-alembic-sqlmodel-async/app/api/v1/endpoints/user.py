from typing import Optional
from app.schemas.common_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IPostResponseBase,
    create_response,
)
from fastapi_pagination import Page, Params
from app.schemas.user_schema import (
    IUserCreate,
    IUserRead,
    IUserReadWithoutGroups,
    IUserStatus,
)
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app import crud
from app.models import User
from sqlmodel import select, and_
from uuid import UUID
from app.schemas.role_schema import IRoleEnum
from app.models.role_model import Role

router = APIRouter()


@router.get("/list", response_model=IGetResponseBase[Page[IUserReadWithoutGroups]])
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
    response_model=IGetResponseBase[Page[IUserReadWithoutGroups]],
)
async def read_users_list_by_role_name(
    status: Optional[IUserStatus] = Query(
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
    user_status = True if status == IUserStatus.active else False
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
    response_model=IGetResponseBase[Page[IUserReadWithoutGroups]],
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


@router.get("/{user_id}", response_model=IGetResponseBase[IUserRead])
async def get_user_by_id(
    user_id: UUID,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    """
    Gets a user by its id
    """
    user = await crud.user.get(id=user_id)
    return create_response(data=user)


@router.get("", response_model=IGetResponseBase[IUserRead])
async def get_my_data(
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Gets my user profile information
    """
    return create_response(data=current_user)


@router.post("", response_model=IPostResponseBase[IUserRead])
async def create_user(
    new_user: IUserCreate = Depends(deps.user_exists),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
):
    """
    Creates a new user
    """
    user = await crud.user.create_with_role(obj_in=new_user)
    return create_response(data=user)


@router.delete("/{user_id}", response_model=IDeleteResponseBase[IUserRead])
async def remove_user(
    user_id: UUID = Depends(deps.is_valid_user),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
):
    """
    Deletes a user by its id
    """
    if current_user.id == user_id:
        raise HTTPException(status_code=404, detail="Users can not delete theirselfs")

    user = await crud.user.remove(id=user_id)
    return create_response(data=user)
