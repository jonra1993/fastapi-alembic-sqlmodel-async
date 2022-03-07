from typing import List
from app.schemas.common import (
    IDeleteResponseBase,
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
)
from app.schemas.hero_team import ITeamCreate, ITeamRead, ITeamReadWithHeroes, ITeamUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app import crud

router = APIRouter()


@router.get("/team", response_model=IGetResponseBase[List[ITeamRead]])
async def get_teams_list(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db_session: AsyncSession = Depends(deps.get_db),
):
    teams = await crud.team.get_multi(db_session, skip=skip, limit=limit)
    output = IGetResponseBase(data=teams)
    return output


@router.get("/team/{team_id}", response_model=IGetResponseBase[ITeamReadWithHeroes])
async def get_team_by_id(
    team_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
):
    team = await crud.team.get(db_session, id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team no found")
    output = IGetResponseBase(data=ITeamReadWithHeroes.from_orm(team))
    return output


@router.post("/team", response_model=IPostResponseBase[ITeamCreate])
async def create_team(
    team: ITeamCreate,
    db_session: AsyncSession = Depends(deps.get_db),
):
    heroe = await crud.team.create(db_session, obj_in=team)
    output = IPostResponseBase(data=heroe)
    return output


@router.put("/team/{team_id}", response_model=IPostResponseBase[ITeamRead])
async def update_team(
    team_id: int,
    new_team: ITeamUpdate,
    db_session: AsyncSession = Depends(deps.get_db),
):
    current_hero = await crud.team.get(db_session=db_session, id=team_id)
    if not current_hero:
        raise HTTPException(status_code=404, detail="Team not found")
    heroe_updated = await crud.team.update(
        db_session=db_session, obj_current=current_hero, obj_new=new_team
    )
    print('heroe_updated', heroe_updated)
    output = IPutResponseBase(data=heroe_updated)
    return output


@router.delete("/team/{team_id}", response_model=IDeleteResponseBase[ITeamRead])
async def remove_team(
    team_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
):
    current_hero = await crud.team.get(db_session=db_session, id=team_id)
    if not current_hero:
        raise HTTPException(status_code=404, detail="Team not found")
    heroe = await crud.team.remove(db_session, id=team_id)
    output = IDeleteResponseBase(data=heroe)
    return output
