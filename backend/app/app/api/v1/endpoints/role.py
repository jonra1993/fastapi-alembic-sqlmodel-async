from app.utils.exceptions import (
    ContentNoChangeException,
    NameExistException,
)
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.deps import role_deps
from app.models.role_model import Role
from app.models.user_model import User
from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleCreate, IRoleEnum, IRoleRead, IRoleUpdate

router = APIRouter()


@router.get("")
async def get_roles(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IRoleRead]:
    """
    Gets a paginated list of roles
    """
    roles = await crud.role.get_multi_paginated(params=params)
    return create_response(data=roles)


@router.get("/{role_id}")
async def get_role_by_id(
    role: Role = Depends(role_deps.get_user_role_by_id),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IRoleRead]:
    """
    Gets a role by its id
    """
    return create_response(data=role)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(
    role: IRoleCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
) -> IPostResponseBase[IRoleRead]:
    """
    Create a new role

    Required roles:
    - admin
    """
    role_current = await crud.role.get_role_by_name(name=role.name)
    if role_current:
        raise NameExistException(Role, name=role_current.name)

    new_role = await crud.role.create(obj_in=role)
    return create_response(data=new_role)


@router.put("/{role_id}")
async def update_role(
    role: IRoleUpdate,
    current_role: Role = Depends(role_deps.get_user_role_by_id),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
) -> IPutResponseBase[IRoleRead]:
    """
    Updates a role by its id

    Required roles:
    - admin
    """
    if current_role.name == role.name and current_role.description == role.description:
        raise ContentNoChangeException()

    exist_role = await crud.role.get_role_by_name(name=role.name)
    if exist_role:
        raise NameExistException(Role, name=role.name)

    updated_role = await crud.role.update(obj_current=current_role, obj_new=role)
    return create_response(data=updated_role)
