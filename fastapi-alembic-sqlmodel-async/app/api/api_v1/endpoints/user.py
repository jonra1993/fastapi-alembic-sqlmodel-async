from typing import List
from app.schemas.common import (
    IDeleteResponseBase,
    IGetResponseBase,
    IPostResponseBase,
)
from app.schemas.user import IUserCreate, IUserRead, IUserReadWithoutGroups
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app import crud
from app.models import User
from app.utils.map_schema import map_models_schema

router = APIRouter()


@router.get("/users", response_model=IGetResponseBase[List[IUserReadWithoutGroups]])
async def read_users_list(
    db_session: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Retrieve users.
    """
    users = await crud.user.get_multi(db_session, skip=skip, limit=limit)
    return IGetResponseBase(data=map_models_schema(IUserReadWithoutGroups, users))


@router.get("/user/{user_id}", response_model=IGetResponseBase[IUserRead])
async def get_user_by_id(
    user_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    user = await crud.user.get_user_by_id(db_session, id=user_id)
    return IGetResponseBase(data=IUserRead.from_orm(user))

@router.get("/user", response_model=IGetResponseBase[IUserRead])
async def get_my_data(
    current_user: User = Depends(deps.get_current_active_user),
):
    return IGetResponseBase(data=IUserRead.from_orm(current_user))

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
    return IPostResponseBase(data=IUserRead.from_orm(user))


@router.delete("/user/{user_id}", response_model=IDeleteResponseBase[IUserRead])
async def remove_user(
    user_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=404, detail="Users can not delete theirselfs")

    user = await crud.user.get_user_by_id(db_session=db_session, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User no found")    
    user = await crud.user.remove(db_session, id=user_id)
    output = IDeleteResponseBase(
        data=user
    )
    return output