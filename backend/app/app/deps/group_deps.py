from app import crud
from app.models.group_model import Group
from app.utils.exceptions.common_exception import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated


async def get_group_by_name(
    group_name: Annotated[
        str, Query(description="String compare with name or last name")
    ] = ""
) -> str:
    group = await crud.group.get_group_by_name(name=group_name)
    if not group:
        raise NameNotFoundException(Group, name=group_name)
    return group


async def get_group_by_id(
    group_id: Annotated[UUID, Path(description="The UUID id of the group")]
) -> Group:
    group = await crud.group.get(id=group_id)
    if not group:
        raise IdNotFoundException(Group, id=group_id)
    return group
