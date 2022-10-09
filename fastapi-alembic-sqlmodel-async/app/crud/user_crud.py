from typing import Any, Dict, List, Optional, Union
from app.schemas.media_schema import IMediaCreate
from pydantic.networks import EmailStr
from app.crud.base_crud import CRUDBase
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from app.schemas.user_schema import IUserCreate, IUserUpdate
from app.schemas.media_schema import IImageMediaCreate
from app.models.user_model import User
from app.models.media_model import ImageMedia, Media
from app.core.security import verify_password, get_password_hash
from datetime import datetime
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

class CRUDUser(CRUDBase[User, IUserCreate, IUserUpdate]):
    async def get_by_email(self, *, email: str, db_session: Optional[AsyncSession] = None) -> Optional[User]:
        db_session = db_session or db.session
        users =  await db_session.execute(select(User).where(User.email == email))
        return users.scalar_one_or_none()

    async def create_with_role(self, *, obj_in: IUserCreate, db_session: Optional[AsyncSession] = None) -> User:
        db_session = db_session or db.session
        db_obj = User.from_orm(obj_in)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    
    async def update_is_active(
        self,
        *,
        db_obj: List[User],
        obj_in: Union[int, str, Dict[str, Any]]
    ) -> Union[User, None]:
        response = None
        for x in db_obj:
            setattr(x, "is_active", obj_in.is_active)
            setattr(x, "updated_at", datetime.utcnow())
            db.session.add(x)
            await db.session.commit()
            await db.session.refresh(x)
            response.append(x)
        return response

    async def authenticate(
        self, *, email: EmailStr, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(email=email)        
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def update_photo(self, *, user: User, image: IMediaCreate, heigth: int, width: int, file_format: str) -> User:
        user.image = ImageMedia(media=Media.from_orm(image), height=heigth, width=width, file_format=file_format )
        db.session.add(user)
        await db.session.commit()
        await db.session.refresh(user)
        return user


user = CRUDUser(User)
