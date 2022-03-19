from app.models.user import User
from app.schemas.common import (
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
)
from fastapi_pagination import Page, Params
from app.schemas.group import IGroupCreate, IGroupRead, IGroupReadWithUsers, IGroupUpdate, IGroupReadWithUsers
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, Query, HTTPException
from app.api import deps
from app import crud

router = APIRouter()    

@router.get("/group", response_model=IGetResponseBase[Page[IGroupRead]])
async def get_groups(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    groups = await crud.group.get_multi_paginated(db_session, params=params)
    return IGetResponseBase[Page[IGroupRead]](data=groups)

@router.get("/group/{group_id}", response_model=IGetResponseBase[IGroupReadWithUsers])
async def get_group_by_id(
    group_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    group = await crud.group.get(db_session, id=group_id)
    return IGetResponseBase[IGroupReadWithUsers](data=group)

@router.post("/group", response_model=IPostResponseBase[IGroupRead])
async def create_group(
    group: IGroupCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    new_group = await crud.group.create_group(db_session, obj_in=group, user_id=current_user.id)
    return IPostResponseBase[IGroupRead](data=new_group)  

@router.put("/group/{group_id}", response_model=IPutResponseBase[IGroupRead])
async def update_group(
    group_id: int,
    group: IGroupUpdate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    group_current = await crud.group.get(db_session=db_session, id=group_id)
    if not group_current:
        raise HTTPException(status_code=404, detail="Group not found")

    group_updated = await crud.group.update(db_session, obj_current=group_current, obj_new=group)
    return IPutResponseBase[IGroupRead](data=group_updated)  

@router.post("/group/add_user/{user_id}/{group_id}", response_model=IPostResponseBase[IGroupRead])
async def add_user_to_group(
    user_id: int,
    group_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    user = await crud.user.get(db_session=db_session, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    group = await crud.group.add_user_to_group(db_session, user=user, group_id=group_id)    
    return IPostResponseBase[IGroupRead](message="User added to group", data=group)   
