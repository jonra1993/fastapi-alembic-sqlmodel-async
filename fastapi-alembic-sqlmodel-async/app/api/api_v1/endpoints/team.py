from typing import List
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
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app import crud

router = APIRouter()


@router.get("/team", response_model=IGetResponseBase[Page[ITeamRead]])
async def get_teams_list(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):    
    teams = await crud.team.get_multi_paginated(db_session, params=params, schema=ITeamRead)
    return IGetResponseBase(data=teams)    


@router.get("/team/{team_id}", response_model=IGetResponseBase[ITeamReadWithHeroes])
async def get_team_by_id(
    team_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
):
    team = await crud.team.get(db_session, id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team no found")
    return IGetResponseBase(data=ITeamReadWithHeroes.from_orm(team))    


@router.post("/team", response_model=IPostResponseBase[ITeamRead])
async def create_team(
    team: ITeamCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    team = await crud.team.create_team(db_session, obj_in=team, user_id=current_user.id)
    return IPostResponseBase(data=team)    


@router.put("/team/{team_id}", response_model=IPostResponseBase[ITeamRead])
async def update_team(
    team_id: int,
    new_team: ITeamUpdate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    current_team = await crud.team.get(db_session=db_session, id=team_id)
    if not current_team:
        raise HTTPException(status_code=404, detail="Team not found")
    heroe_updated = await crud.team.update(
        db_session=db_session, obj_current=current_team, obj_new=new_team
    )
    return IPutResponseBase(data=heroe_updated)    


@router.delete("/team/{team_id}", response_model=IDeleteResponseBase[ITeamRead])
async def remove_team(
    team_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)

):
    current_team = await crud.team.get(db_session=db_session, id=team_id)
    if not current_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team = await crud.team.remove(db_session, id=team_id)
    return IDeleteResponseBase(data=team)
