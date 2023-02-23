from app import crud
from app.models.role_model import Role
from app.utils.exceptions.common_exception import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query


async def get_user_role_by_name(
    role_name: str = Query(
        default="", description="String compare with name or last name"
    )
) -> str:
    role = await crud.role.get_role_by_name(name=role_name)
    if not role:
        raise NameNotFoundException(Role, name=role_name)
    return role_name


async def get_user_role_by_id(id: UUID) -> Role:
    role = await crud.role.get(id=id)
    if not role:
        raise IdNotFoundException(Role, id=id)
    return role
