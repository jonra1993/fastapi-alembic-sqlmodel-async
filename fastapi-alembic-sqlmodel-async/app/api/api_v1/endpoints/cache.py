from datetime import datetime
from typing import Optional, Union

from fastapi import APIRouter
from app.schemas.common import (
    IGetResponseBase,
)
from fastapi_cache.decorator import cache

router = APIRouter()


@router.get("/cache/cached", response_model=IGetResponseBase[Union[str, datetime]])
@cache(expire=10)
async def get_a_cached_response():
    """
    Get a cached datetime
    """    
    return IGetResponseBase[Union[str, datetime]](data=datetime.now())


@router.get("/cache/no_cached", response_model=IGetResponseBase[Union[str, datetime]])
async def get_a_normal_response():
    """
    Get a real-time datetime
    """    
    return IGetResponseBase[Union[str, datetime]](data=datetime.now())