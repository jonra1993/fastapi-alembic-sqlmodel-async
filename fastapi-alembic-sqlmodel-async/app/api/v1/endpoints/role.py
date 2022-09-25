from app.models.user_model import User
from app.schemas.common_schema import (
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from fastapi_pagination import Page, Params
from app.schemas.role_schema import IRoleCreate, IRoleRead, IRoleUpdate
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app import crud
from uuid import UUID
from app.schemas.role_schema import IRoleEnum

router = APIRouter()


@router.get("", response_model=IGetResponseBase[Page[IRoleRead]])
async def get_roles(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Gets a paginated list of roles
    """
    roles = await crud.role.get_multi_paginated(params=params)
    return create_response(data=roles)


@router.get("/{role_id}", response_model=IGetResponseBase[IRoleRead])
async def get_role_by_id(
    role_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Gets a role by its id
    """
    role = await crud.role.get(id=role_id)
    return create_response(data=role)


@router.post("", response_model=IPostResponseBase[IRoleRead])
async def create_role(
    role: IRoleCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
):
    """
    Create a new role
    """
    new_permission = await crud.role.create(obj_in=role)
    return create_response(data=new_permission)


@router.put("/{role_id}", response_model=IPutResponseBase[IRoleRead])
async def update_permission(
    role_id: UUID,
    role: IRoleUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
):
    """
    Updates the permission of a role by its id
    """
    current_role = await crud.role.get(id=role_id)
    if not current_role:
        raise HTTPException(status_code=404, detail="Permission not found")

    updated_role = await crud.role.update(obj_current=current_role, obj_new=role)
    return create_response(data=updated_role)
