from app.schemas.role import IRoleCreate, IRoleUpdate
from app.models.role import Role
from app.models.user import User
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

class CRUDRole(CRUDBase[Role, IRoleCreate, IRoleUpdate]):
    async def get_role_by_name(self, db_session: AsyncSession, *, name: str) -> Role:
        role = await db_session.exec(select(Role).where(Role.name == name))
        return role.first()

    async def add_role_to_user(self, db_session: AsyncSession, *, user: User, role_id: UUID) -> Role:
        role = await super().get(db_session, id=role_id)
        role.users.append(user)        
        db_session.add(role)
        await db_session.commit()
        await db_session.refresh(role)
        return role


role = CRUDRole(Role)
