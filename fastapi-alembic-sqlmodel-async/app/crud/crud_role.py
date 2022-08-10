from typing import Optional
from app.schemas.role import IRoleCreate, IRoleUpdate
from app.models.role import Role
from app.models.user import User
from app.crud.base_sqlmodel import CRUDBase
from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

class CRUDRole(CRUDBase[Role, IRoleCreate, IRoleUpdate]):
    async def get_role_by_name(self, *, name: str, db_session: Optional[AsyncSession] = None) -> Role:
        if db_session == None:
            db_session = db.session()
        role = await db_session.execute(select(Role).where(Role.name == name))
        return role.scalar_one_or_none()

    async def add_role_to_user(self, *, user: User, role_id: UUID) -> Role:
        role = await super().get(id=role_id)
        role.users.append(user)        
        db.session.add(role)
        await db.session.commit()
        await db.session.refresh(role)
        return role


role = CRUDRole(Role)
