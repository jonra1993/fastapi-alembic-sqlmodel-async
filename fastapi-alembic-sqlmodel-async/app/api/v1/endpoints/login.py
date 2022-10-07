from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from app.core.security import get_password_hash
from app.core.security import verify_password
from app.models.user_model import User
from app.api.deps import get_redis_client
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import EmailStr
from pydantic import ValidationError
from app import crud
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.token_schema import TokenRead, Token, RefreshToken
from app.schemas.common_schema import IMetaGeneral, IPostResponseBase, create_response
from aioredis import Redis
from enum import Enum

router = APIRouter()


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


async def add_token_to_redis(
    redis_client: Redis, user: User, token: str, token_type: TokenType, expire_time: int
):
    token_key = f"user:{user.id}:{token_type}"
    print("token_key", token_key)
    await redis_client.sadd(token_key, token)
    await redis_client.expire(token_key, expire_time)
    print("done")


async def delete_tokens(redis_client: Redis, user: User, token_type: TokenType):
    token_key = f"user:{user.id}:{token_type}"
    await redis_client.delete(token_key)


@router.post("", response_model=IPostResponseBase[Token])
async def login(
    email: EmailStr = Body(...),
    password: str = Body(...),
    meta_data: IMetaGeneral = Depends(deps.get_general_meta),
    redis_client: Redis = Depends(get_redis_client),
) -> Any:
    """
    Login for all users
    """
    user = await crud.user.authenticate(email=email, password=password)
    if not user:
        raise HTTPException(status_code=400, detail="Email or Password incorrect")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="User is inactive")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(
        user.id, expires_delta=refresh_token_expires
    )
    data = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        user=user,
    )
    await add_token_to_redis(
        redis_client,
        user,
        access_token,
        TokenType.ACCESS,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    await add_token_to_redis(
        redis_client,
        user,
        refresh_token,
        TokenType.REFRESH,
        settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )

    return create_response(meta=meta_data, data=data, message="Login correctly")


@router.post("/change_password", response_model=IPostResponseBase[Token])
async def change_password(
    current_password: str = Body(...),
    new_password: str = Body(...),
    current_user: User = Depends(deps.get_current_user()),
    redis_client: Redis = Depends(get_redis_client),
) -> Any:
    """
    Change password
    """

    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Current Password")

    hashed_password = get_password_hash(new_password)
    await crud.user.update(
        obj_current=current_user, obj_new={"hashed_password": hashed_password}
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        current_user.id, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(
        current_user.id, expires_delta=refresh_token_expires
    )
    data = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        user=current_user,
    )

    await delete_tokens(redis_client, current_user, TokenType.ACCESS)
    await delete_tokens(redis_client, current_user, TokenType.REFRESH)
    await add_token_to_redis(
        redis_client,
        current_user,
        access_token,
        TokenType.ACCESS,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    await add_token_to_redis(
        redis_client,
        current_user,
        refresh_token,
        TokenType.REFRESH,
        settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )

    return create_response(data=data, message="New password generated")


@router.post(
    "/refresh_token", response_model=IPostResponseBase[TokenRead], status_code=201
)
async def get_refresh_token(
    body: RefreshToken = Body(...),
    redis_client: Redis = Depends(get_redis_client),
) -> Any:
    """
    Gets a refresh token
    """
    try:
        payload = jwt.decode(
            body.refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Refresh token invalid")

    if payload["type"] == "refresh":
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        user = await crud.user.get(id=payload["sub"])
        if user.is_active:
            access_token = security.create_access_token(
                payload["sub"], expires_delta=access_token_expires
            )
            await add_token_to_redis(
                redis_client,
                user,
                access_token,
                TokenType.ACCESS,
                settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            )
            return create_response(
                data=TokenRead(access_token=access_token, token_type="bearer"),
                message="Access token generated correctly",
            )
        else:
            raise HTTPException(status_code=404, detail="User inactive")
    else:
        raise HTTPException(status_code=404, detail="Incorrect token")


@router.post("/access-token", response_model=TokenRead)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    redis_client: Redis = Depends(get_redis_client),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    await add_token_to_redis(
        redis_client,
        user,
        access_token,
        TokenType.ACCESS,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
