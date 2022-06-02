from typing import AsyncGenerator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.models.user import User
from pydantic import ValidationError
from app import crud
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.common import IMetaGeneral
from app.db.auth_session import AuthContextManager

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_auth_session():
    with AuthContextManager() as auth:
        return auth

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_general_meta(
    db_session: AsyncSession = Depends(get_db)
) -> IMetaGeneral:
    current_roles = await crud.role.get_multi(db_session, skip=0, limit=100)
    return IMetaGeneral(roles=current_roles)

def get_current_user(required_roles: List[str] = None) -> User:
    async def current_user(
            db_session: AsyncSession = Depends(get_db),
            token: str = Depends(reusable_oauth2)
    ) -> User:        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user: User = await crud.user.get_user_by_id(db_session, id=payload["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        if required_roles:
            is_valid_role = False
            for role in required_roles:
                if role == user.role.name:
                    is_valid_role = True
                    
            if is_valid_role == False:
                raise HTTPException(
                    status_code=403,
                    detail=f'Role "{required_roles}" is required to perform this action',
                )
        
        return user

    return current_user



