from datetime import datetime, timedelta, date
from app import crud
from typing import Union
from fastapi import APIRouter, Query
from app.schemas.response_schema import IGetResponseBase, create_response
from fastapi_cache.decorator import cache

router = APIRouter()


@router.get("/cached", response_model=IGetResponseBase[Union[str, datetime]])
@cache(expire=10)
async def get_a_cached_response():
    """
    Gets a cached datetime
    """
    return create_response(data=datetime.now())


@router.get("/no_cached", response_model=IGetResponseBase[Union[str, datetime]])
async def get_a_normal_response():
    """
    Gets a real-time datetime
    """
    return create_response(data=datetime.now())


@router.get("/heroe_count/cached", response_model=IGetResponseBase[int])
@cache(expire=20)
async def get_count_of_heroes_created_cached(
    start_date: date = Query(default=(datetime.now() - timedelta(days=7)).date()),
    end_date: date = Query(default=datetime.now().date()),
):
    """
    Gets count of heroes created on a base time (Cached response)
    """
    count = await crud.hero.get_count_of_heroes(
        start_time=datetime.combine(start_date, datetime.min.time()),
        end_time=datetime.combine(end_date, datetime.min.time()),
    )
    return create_response(message="message", data=count)


@router.get("/heroe_count/no_cached", response_model=IGetResponseBase[int])
async def get_count_of_heroes_created_no_cached(
    start_date: date = Query(default=(datetime.now() - timedelta(days=7)).date()),
    end_date: date = Query(default=datetime.now().date()),
):
    """
    Gets count of heroes created on a base time (No Cached response)
    """
    count = await crud.hero.get_count_of_heroes(
        start_time=datetime.combine(start_date, datetime.min.time()),
        end_time=datetime.combine(end_date, datetime.min.time()),
    )
    return create_response(message="", data=count)
