from typing import List
from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from typing import Dict
from asyncer import asyncify, create_task_group, syncify
from app.core.config import settings
import httpx
from app.schemas.response_schema import IGetResponseBase, create_response

router = APIRouter()

api_reference: Dict[str, str] = {"api_reference": "https://github.com/chubin/wttr.in"}


def get_weather_sync(city: str):
    """
    Gets weather by goweather API with sync client
    """
    response = httpx.get(f"{settings.WHEATER_URL}/{city}?format=j1")
    weather = response.json()
    weather["city"] = city
    return weather


async def get_weather_async(city: str):
    """
    Gets weather by goweather API with async client
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.WHEATER_URL}/{city}?format=j1")
        weather = response.json()
        weather["city"] = city
        return weather


def do_sync_work(city: str):
    """
    Gets weather by sync work
    """
    # This similar aproach will be used to interface with celery
    weather = syncify(get_weather_async)(city=city)
    return weather


@router.get("/weather_sync/sync1", response_model=IGetResponseBase)
@cache(expire=10)
async def get_weather_sync_work_by_city(
    city: str = Query(default="Quito"),
):
    """
    Gets Weather by city using sync work
    """
    weather = await asyncify(do_sync_work)(city=city)
    return create_response(
        message=f"Weather in {city}", data=weather, meta=api_reference
    )


@router.get("/weather_sync/sync2", response_model=IGetResponseBase)
@cache(expire=10)
async def get_weather_sync_client_by_city(
    city: str = Query(default="Quito"),
):
    """
    Gets Weather by city using sync client
    """
    weather = await asyncify(get_weather_sync)(city=city)
    return create_response(
        message=f"Weather in {city}", data=weather, meta=api_reference
    )


@router.get("/weather_async", response_model=IGetResponseBase)
@cache(expire=10)
async def get_weather_async_client_by_city(
    city: str = Query(default="Quito"),
):
    """
    Gets Weather by city using async client
    """
    weather = await get_weather_async(city=city)
    return create_response(
        message=f"Weather in {city}", data=weather, meta=api_reference
    )


@router.get("/weather_async_list/sequencial", response_model=IGetResponseBase)
@cache(expire=10)
async def get_weather_async_sequencial_by_cities(
    cities: List[str] = Query(default=["Quito", "Miami", "Barcelona"]),
):
    """
    Gets Weather by list of cities
    It does sequencial requests
    """
    weather_list = []
    for city in cities:
        weather = await get_weather_async(city=city)
        weather_list.append(weather)

    return create_response(
        message=f"Weather in {', '.join(cities)}", data=weather_list, meta=api_reference
    )


@router.get("/weather_async_list/concurrent", response_model=IGetResponseBase)
@cache(expire=10)
async def get_weather_async_concurrent_by_cities(
    cities: List[str] = Query(default=["Quito", "Miami", "Barcelona"]),
):
    """
    Gets Weather by list of cities
    It it optimized to do concurrent requests (It is faster than sequencial endpoint)
    """
    weather_list = [{}] * len(cities)
    async with create_task_group() as task_group:
        for index, city in enumerate(cities):
            weather_list[index] = task_group.soonify(get_weather_async)(city=city)

    weather_list = list(map(lambda weather: weather.value, weather_list))
    return create_response(
        message=f"Weather in {', '.join(cities)}", data=weather_list, meta=api_reference
    )
