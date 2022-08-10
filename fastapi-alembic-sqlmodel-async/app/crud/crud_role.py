from app.schemas.role import IRoleCreate, IRoleUpdate
from app.models.role import Role
from app.models.user import User
from app.crud.base_sqlmodel import CRUDBase
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from uuid import UUID

class CRUDRole(CRUDBase[Role, IRoleCreate, IRoleUpdate]):
    async def get_role_by_name(self, *, name: str) -> Role:
        role = await db.session.execute(select(Role).where(Role.name == name))
        return role.first()

    async def add_role_to_user(self, *, user: User, role_id: UUID) -> Role:
        role = await super().get(id=role_id)
        role.users.append(user)        
        db.session.add(role)
        await db.session.commit()
        await db.session.refresh(role)
        return role


role = CRUDRole(Role)
