from typing import List
from app.models.user import User
from app.schemas.common import (
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
)
from app.schemas.role import IRoleCreate, IRoleRead, IRoleUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, Query, HTTPException
from app.api import deps
from app import crud

router = APIRouter()    

@router.get("/role", response_model=IGetResponseBase[List[IRoleRead]])
async def get_roles(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    roles = await crud.role.get_multi(db_session, skip=skip, limit=limit)   
    return IGetResponseBase(data=roles)

@router.get("/role/{role_id}", response_model=IGetResponseBase[IRoleRead])
async def get_role_by_id(
    role_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    role = await crud.role.get(db_session, id=role_id)
    return IGetResponseBase(data=role)

@router.post("/role", response_model=IPostResponseBase[IRoleRead])
async def create_role(
    role: IRoleCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    new_permission = await crud.role.create(db_session, obj_in=role)
    return IPostResponseBase(data=new_permission)  

@router.put("/role/{role_id}", response_model=IPutResponseBase[IRoleRead])
async def update_permission(
    role_id: int,
    role: IRoleUpdate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    current_role = await crud.role.get(db_session=db_session, id=role_id)
    if not current_role:
        raise HTTPException(status_code=404, detail="Permission not found")

    updated_role = await crud.role.update(db_session, obj_current=current_role, obj_new=role)
    return IPutResponseBase(data=updated_role)  

