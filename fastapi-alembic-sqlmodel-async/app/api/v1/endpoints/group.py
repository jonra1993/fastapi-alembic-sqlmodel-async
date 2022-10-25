from app.models.user_model import User
from app.schemas.response_schema import (
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
    IGetResponsePaginated,
    create_response,
)
from fastapi_pagination import Params
from app.schemas.group_schema import (
    IGroupCreate,
    IGroupRead,
    IGroupReadWithUsers,
    IGroupUpdate,
    IGroupReadWithUsers,
)
from fastapi import APIRouter, Depends, HTTPException, status
from app.api import deps
from app import crud
from uuid import UUID
from app.schemas.role_schema import IRoleEnum

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group id is invalid")

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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group name already exists")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    
    if group_current.name == group.name and group_current.description == group.description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The content has not changed")

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    group = await crud.group.get(id=group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    group = await crud.group.add_user_to_group(user=user, group_id=group_id)
    return create_response(message="User added to group", data=group)
