from app.schemas.common import (
    IDeleteResponseBase,
    IGetResponseBase,
    IPostResponseBase,
)
from fastapi_pagination import Page, Params
from app.schemas.user import IUserCreate, IUserRead, IUserReadWithoutGroups
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app import crud
from app.models import User
from sqlmodel import select
from uuid import UUID

router = APIRouter()


@router.get("/user", response_model=IGetResponseBase[Page[IUserReadWithoutGroups]])
async def read_users_list(    
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user()),
):
    """
    Retrieve users.
    """    
    users = await crud.user.get_multi_paginated(db_session, params=params)
    return IGetResponseBase[Page[IUserReadWithoutGroups]](data=users)

@router.get("/user/order_by_created_at", response_model=IGetResponseBase[Page[IUserReadWithoutGroups]])
async def get_hero_list_order_by_created_at(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user()),
):
    query = select(User).order_by(User.created_at)
    users = await crud.user.get_multi_paginated(db_session, query=query, params=params)
    return IGetResponseBase[Page[IUserReadWithoutGroups]](data=users)

@router.get("/user/{user_id}", response_model=IGetResponseBase[IUserRead])
async def get_user_by_id(
    user_id: UUID,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user()),
):
    user = await crud.user.get_user_by_id(db_session, id=user_id)
    return IGetResponseBase[IUserRead](data=user)

@router.get("/user", response_model=IGetResponseBase[IUserRead])
async def get_my_data(
    current_user: User = Depends(deps.get_current_user()),
):
    return IGetResponseBase[IUserRead](data=current_user)

@router.post("/user", response_model=IPostResponseBase[IUserRead])
async def create_user(
    new_user: IUserCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):    
    user = await crud.user.get_by_email(db_session, email=new_user.email)
    if user:
        raise HTTPException(status_code=404, detail="There is already a user with same email")
    user = await crud.user.create(db_session, obj_in=new_user)
    return IPostResponseBase[IUserRead](data=user)


@router.delete("/user/{user_id}", response_model=IDeleteResponseBase[IUserRead])
async def remove_user(
    user_id: UUID,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=404, detail="Users can not delete theirselfs")

    user = await crud.user.get_user_by_id(db_session=db_session, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User no found")    
    user = await crud.user.remove(db_session, id=user_id)
    return IDeleteResponseBase[IUserRead](
        data=user
    )
