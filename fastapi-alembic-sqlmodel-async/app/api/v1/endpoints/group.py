from uuid import UUID

from app import crud
from app.api import deps
from app.models.group_model import Group
from app.models.user_model import User
from app.schemas.group_schema import (
    IGroupCreate,
    IGroupRead,
    IGroupReadWithUsers,
    IGroupUpdate,
)
from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleEnum
from app.utils.exceptions import (
    ContentNoChangeException,
    IdNotFoundException,
    NameExistException,
)
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

router = APIRouter()


@router.get("", response_model=IGetResponsePaginated[IGroupRead])
async def get_groups(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Gets a paginated list of groups
    """
    groups = await crud.group.get_multi_paginated(params=params)
    return create_response(data=groups)


@router.get("/{group_id}", response_model=IGetResponseBase[IGroupReadWithUsers])
async def get_group_by_id(
    group_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Gets a group by its id
    """
    group = await crud.group.get(id=group_id)
    if group:
        return create_response(data=group)
    else:
        raise IdNotFoundException(Group, group_id)


@router.post("", response_model=IPostResponseBase[IGroupRead], status_code=status.HTTP_201_CREATED)
async def create_group(
    group: IGroupCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    """
    Creates a new group
    """
    group_current = await crud.group.get_group_by_name(name=group.name)
    if group_current:
        raise NameExistException(Group, name=group.name)
    new_group = await crud.group.create(obj_in=group, created_by_id=current_user.id)
    return create_response(data=new_group)


@router.put("/{group_id}", response_model=IPutResponseBase[IGroupRead])
async def update_group(
    group_id: UUID,
    group: IGroupUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    """
    Updates a group by its id
    """
    group_current = await crud.group.get(id=group_id)
    if not group_current:
        raise IdNotFoundException(Group, group_id=group_id)

    if group_current.name == group.name and group_current.description == group.description:
        raise ContentNoChangeException()

    group_updated = await crud.group.update(obj_current=group_current, obj_new=group)
    return create_response(data=group_updated)


@router.post(
    "/add_user/{user_id}/{group_id}", response_model=IPostResponseBase[IGroupRead]
)
async def add_user_into_a_group(
    user_id: UUID,
    group_id: UUID,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
):
    """
    Adds a user into a group
    """
    user = await crud.user.get(id=user_id)
    if not user:
        raise IdNotFoundException(User, id=user_id)

    group = await crud.group.get(id=group_id)
    if not group:
        raise IdNotFoundException(Group, group_id)

    group = await crud.group.add_user_to_group(user=user, group_id=group_id)
    return create_response(message="User added to group", data=group)
