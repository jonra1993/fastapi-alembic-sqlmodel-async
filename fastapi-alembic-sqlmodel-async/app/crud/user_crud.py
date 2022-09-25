from typing import Any, Dict, List, Optional, Union
from pydantic.networks import EmailStr
from app.crud.base_crud import CRUDBase
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from app.schemas.user_schema import IUserCreate, IUserUpdate
from app.models.user_model import User
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
        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            is_superuser=obj_in.is_superuser,
            hashed_password=get_password_hash(obj_in.password),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            role_id=obj_in.role_id
        )
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: User,
        obj_in: Union[IUserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data["updated_at"] = datetime.utcnow()
        update_data["first_name"] = obj_in.first_name
        update_data["last_name"] = obj_in.last_name

        response = super().update(db.session, db_obj=db_obj, obj_in=update_data)
        return response

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


user = CRUDUser(User)
