from app.models.user_model import User
from app.schemas.response_schema import (
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
    IGetResponsePaginated,
    create_response,
)
from fastapi_pagination import Params
from app.schemas.role_schema import IRoleCreate, IRoleRead, IRoleUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from app.api import deps
from app import crud
from uuid import UUID
from app.schemas.role_schema import IRoleEnum

router = APIRouter()


@router.get("", response_model=IGetResponsePaginated[IRoleRead])
async def get_roles(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Gets a paginated list of roles
    """
    roles = await crud.role.get_multi_paginated(params=params)
    return create_response(data=roles)


@router.get("/{role_id}", response_model=IGetResponseBase[IRoleRead], status_code=status.HTTP_200_OK)
async def get_role_by_id(
    role_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Gets a role by its id
    """
    role = await crud.role.get(id=role_id)
    if role:
        return create_response(data=role)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role id is invalid")


@router.post("", response_model=IPostResponseBase[IRoleRead], status_code=status.HTTP_201_CREATED)
async def create_role(
    role: IRoleCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
):
    """
    Create a new role
    """
    role_current = await crud.role.get_role_by_name(name=role.name)
    if not role_current:
        new_permission = await crud.role.create(obj_in=role)
        return create_response(data=new_permission)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role name already exists") 


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    if current_role.name == role.name and current_role.description == role.description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The content has not changed")

    exist_role = await crud.role.get_role_by_name(name=role.name)
    if exist_role:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role name already exists")
    
    updated_role = await crud.role.update(obj_current=current_role, obj_new=role)
    return create_response(data=updated_role)
