from typing import List
from app.models.group import Group
from app.models.user import User
from app.schemas.group import IGroupCreate, IGroupUpdate
from app.crud.base_sqlmodel import CRUDBase
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from uuid import UUID

class CRUDGroup(CRUDBase[Group, IGroupCreate, IGroupUpdate]):
    async def get_group_by_name(self, *, name: str) -> Group:
        group = await db.session.execute(select(Group).where(Group.name == name))
        return group.first()

    async def add_user_to_group(self, *, user: User, group_id: UUID) -> Group:
        group = await super().get(id=group_id)
        group.users.append(user)        
        db.session.add(group)
        await db.session.commit()
        await db.session.refresh(group)
        return group

    async def add_users_to_group(self, *, users: List[User], group_id: UUID) -> Group:
        group = await super().get(id=group_id)
        group.users.extend(users)        
        db.session.add(group)
        await db.session.commit()
        await db.session.refresh(group)
        return group

group = CRUDGroup(Group)
