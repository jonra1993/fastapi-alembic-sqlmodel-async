from typing import Optional
from uuid import UUID
from app.utils.exceptions import IdNotFoundException, NameNotFoundException
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.models.hero_model import Hero
from app.models.user_model import User
from app.schemas.common_schema import IOrderEnum
from app.schemas.hero_schema import (
    IHeroCreate,
    IHeroRead,
    IHeroReadWithTeam,
    IHeroUpdate,
)
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleEnum

router = APIRouter()


@router.get("")
async def get_hero_list(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IHeroReadWithTeam]:
    """
    Gets a paginated list of heroes
    """
    heroes = await crud.hero.get_multi_paginated(params=params)
    return create_response(data=heroes)


@router.get("/get_by_created_at")
async def get_hero_list_order_by_created_at(
    order: Optional[IOrderEnum] = Query(
        default=IOrderEnum.ascendent, description="It is optional. Default is ascendent"
    ),
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IHeroReadWithTeam]:
    """
    Gets a paginated list of heroes ordered by created at datetime
    """
    heroes = await crud.hero.get_multi_paginated_ordered(
        params=params, order_by="created_at", order=order
    )
    return create_response(data=heroes)


@router.get("/get_by_id/{hero_id}")
async def get_hero_by_id(
    hero_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IHeroReadWithTeam]:
    """
    Gets a hero by its id
    """
    hero = await crud.hero.get(id=hero_id)
    if not hero:
        raise IdNotFoundException(Hero, hero_id)
    return create_response(data=hero)


@router.get("/get_by_name/{hero_name}")
async def get_hero_by_name(
    hero_name: str,
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IHeroReadWithTeam]:
    """
    Gets a hero by his/her name
    """
    hero = await crud.hero.get_heroe_by_name(name=hero_name)
    if not hero:
        raise NameNotFoundException(Hero, hero_name)
    return create_response(data=hero)


@router.post("")
async def create_hero(
    hero: IHeroCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPostResponseBase[IHeroRead]:
    """
    Creates a new hero
    """
    heroe = await crud.hero.create(obj_in=hero, created_by_id=current_user.id)
    return create_response(data=heroe)


@router.put("/{hero_id}")
async def update_hero(
    hero_id: UUID,
    hero: IHeroUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPutResponseBase[IHeroRead]:
    """
    Updates a hero by its id
    """
    current_hero = await crud.hero.get(id=hero_id)
    if not current_hero:
        raise IdNotFoundException(Hero, hero_id)
    heroe_updated = await crud.hero.update(obj_new=hero, obj_current=current_hero)
    return create_response(data=heroe_updated)


@router.delete("/{hero_id}")
async def remove_hero(
    hero_id: UUID,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IDeleteResponseBase[IHeroRead]:
    """
    Deletes a hero by its id
    """
    current_hero = await crud.hero.get(id=hero_id)
    if not current_hero:
        raise IdNotFoundException(Hero, hero_id)
    heroe = await crud.hero.remove(id=hero_id)
    return create_response(data=heroe)
