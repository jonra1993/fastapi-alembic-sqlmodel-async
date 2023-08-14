from uuid import UUID
from app.utils.exceptions import (
    ContentNoChangeException,
    IdNotFoundException,
    NameExistException,
)
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.models.team_model import Team
from app.models.user_model import User
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleEnum
from app.schemas.team_schema import (
    ITeamCreate,
    ITeamRead,
    ITeamUpdate,
)


router = APIRouter()


@router.get("")
async def get_teams_list(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[ITeamRead]:
    """
    Gets a paginated list of teams
    """
    teams = await crud.team.get_multi_paginated(params=params)
    return create_response(data=teams)


@router.get("/{team_id}")
async def get_team_by_id(
    team_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[ITeamRead]:
    """
    Gets a team by its id
    """
    team = await crud.team.get(id=team_id)
    if not team:
        raise IdNotFoundException(Team, id=team_id)
    return create_response(data=team)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_team(
    team: ITeamCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPostResponseBase[ITeamRead]:
    """
    Creates a new team

    Required roles:
    - admin
    - manager
    """
    team_current = await crud.team.get_team_by_name(name=team.name)
    if team_current:
        raise NameExistException(Team, name=team_current.name)
    team = await crud.team.create(obj_in=team, created_by_id=current_user.id)
    return create_response(data=team)


@router.put("/{team_id}")
async def update_team(
    team_id: UUID,
    new_team: ITeamUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPostResponseBase[ITeamRead]:
    """
    Update a team by its id

    Required roles:
    - admin
    - manager
    """
    current_team = await crud.team.get(id=team_id)
    if not current_team:
        raise IdNotFoundException(Team, id=team_id)

    if (
        current_team.name == new_team.name
        and current_team.headquarters == new_team.headquarters
    ):
        raise ContentNoChangeException(detail="The content has not changed")

    exist_team = await crud.team.get_team_by_name(name=new_team.name)
    if exist_team:
        raise NameExistException(Team, name=exist_team.name)

    heroe_updated = await crud.team.update(obj_current=current_team, obj_new=new_team)
    return create_response(data=heroe_updated)


@router.delete("/{team_id}")
async def remove_team(
    team_id: UUID,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IDeleteResponseBase[ITeamRead]:
    """
    Deletes a team by its id

    Required roles:
    - admin
    - manager
    """
    current_team = await crud.team.get(id=team_id)
    if not current_team:
        raise IdNotFoundException(Team, id=team_id)
    team = await crud.team.remove(id=team_id)
    return create_response(data=team)
