from app import crud
from app.models.role_model import Role
from app.utils.exceptions.common_exception import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated


async def get_user_role_by_name(
    role_name: Annotated[str, Query(title="String compare with name or last name")] = ""
) -> str:
    role = await crud.role.get_role_by_name(name=role_name)
    if not role:
        raise NameNotFoundException(Role, name=role_name)
    return role_name


async def get_user_role_by_id(
    role_id: Annotated[UUID, Path(title="The UUID id of the role")]
) -> Role:
    role = await crud.role.get(id=role_id)
    if not role:
        raise IdNotFoundException(Role, id=role_id)
    return role
