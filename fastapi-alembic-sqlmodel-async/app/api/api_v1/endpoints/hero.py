from app.models.user import User
from app.models.hero import Hero
from app.schemas.common import (
    IDeleteResponseBase,
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
)
from fastapi_pagination import Page, Params
from app.schemas.hero import IHeroCreate, IHeroRead, IHeroReadWithTeam, IHeroUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from sqlmodel import select
from app import crud

router = APIRouter()


@router.get("/hero", response_model=IGetResponseBase[Page[IHeroReadWithTeam]])
async def get_hero_list(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    heroes = await crud.hero.get_multi_paginated(db_session, params=params)
    return IGetResponseBase[Page[IHeroReadWithTeam]](data=heroes)

@router.get("/hero/by_created_at", response_model=IGetResponseBase[Page[IHeroReadWithTeam]])
async def get_hero_list_order_by_created_at(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    query = select(Hero).order_by(Hero.created_at)
    heroes = await crud.hero.get_multi_paginated(db_session, query=query, params=params)
    return IGetResponseBase[Page[IHeroReadWithTeam]](data=heroes)

@router.get("/hero/{hero_id}", response_model=IGetResponseBase[IHeroReadWithTeam])
async def get_hero_by_id(
    hero_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    hero = await crud.hero.get(db_session, id=hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return IGetResponseBase[IHeroReadWithTeam](data=hero)


@router.post("/hero", response_model=IPostResponseBase[IHeroRead])
async def create_hero(
    hero: IHeroCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    heroe = await crud.hero.create_hero(db_session, obj_in=hero, user_id=current_user.id)
    return IPostResponseBase[IHeroRead](data=heroe)


@router.put("/hero/{hero_id}", response_model=IPutResponseBase[IHeroRead])
async def update_hero(
    hero_id: int,
    hero: IHeroUpdate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    current_hero = await crud.hero.get(db_session=db_session, id=hero_id)
    if not current_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    heroe_updated = await crud.hero.update(
        db_session=db_session, obj_new=hero, obj_current=current_hero
    )
    return IPutResponseBase[IHeroRead](data=heroe_updated)



@router.delete("/hero/{hero_id}", response_model=IDeleteResponseBase[IHeroRead])
async def remove_hero(
    hero_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    current_hero = await crud.hero.get(db_session=db_session, id=hero_id)
    if not current_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    heroe = await crud.hero.remove(db_session, id=hero_id)
    return IDeleteResponseBase[IHeroRead](data=heroe)

