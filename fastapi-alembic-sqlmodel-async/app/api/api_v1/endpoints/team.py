from app.models.user import User
from app.schemas.common import (
    IDeleteResponseBase,
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
)
from fastapi_pagination import Page, Params
from app.schemas.team import ITeamCreate, ITeamRead, ITeamReadWithHeroes, ITeamUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app import crud
from uuid import UUID
from app.schemas.role import IRoleEnum

router = APIRouter()


@router.get("/team", response_model=IGetResponseBase[Page[ITeamRead]])
async def get_teams_list(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user()),
):    
    teams = await crud.team.get_multi_paginated(db_session, params=params)
    return IGetResponseBase[Page[ITeamRead]](data=teams)    


@router.get("/team/{team_id}", response_model=IGetResponseBase[ITeamReadWithHeroes])
async def get_team_by_id(
    team_id: UUID,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user()),
):
    team = await crud.team.get(db_session, id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team no found")
    return IGetResponseBase[ITeamReadWithHeroes](data=team)


@router.post("/team", response_model=IPostResponseBase[ITeamRead])
async def create_team(
    team: ITeamCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])),
):
    team = await crud.team.create(db_session, obj_in=team, created_by_id=current_user.id)
    return IPostResponseBase[ITeamRead](data=team)    


@router.put("/team/{team_id}", response_model=IPostResponseBase[ITeamRead])
async def update_team(
    team_id: UUID,
    new_team: ITeamUpdate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])),
):
    current_team = await crud.team.get(db_session=db_session, id=team_id)
    if not current_team:
        raise HTTPException(status_code=404, detail="Team not found")
    heroe_updated = await crud.team.update(
        db_session=db_session, obj_current=current_team, obj_new=new_team
    )
    return IPutResponseBase[ITeamRead](data=heroe_updated)    


@router.delete("/team/{team_id}", response_model=IDeleteResponseBase[ITeamRead])
async def remove_team(
    team_id: UUID,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])),

):
    current_team = await crud.team.get(db_session=db_session, id=team_id)
    if not current_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team = await crud.team.remove(db_session, id=team_id)
    return IDeleteResponseBase[ITeamRead](data=team)
