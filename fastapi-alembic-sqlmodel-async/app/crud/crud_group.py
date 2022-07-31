from typing import List
from app.models.group import Group
from app.models.user import User
from app.schemas.group import IGroupCreate, IGroupUpdate
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

class CRUDGroup(CRUDBase[Group, IGroupCreate, IGroupUpdate]):
    async def get_group_by_name(self, db_session: AsyncSession, *, name: str) -> Group:
        group = await db_session.exec(select(Group).where(Group.name == name))
        return group.first()

    async def add_user_to_group(self, db_session: AsyncSession, *, user: User, group_id: UUID) -> Group:
        group = await super().get(db_session, id=group_id)
        group.users.append(user)        
        db_session.add(group)
        await db_session.commit()
        await db_session.refresh(group)
        return group

    async def add_users_to_group(self, db_session: AsyncSession, *, users: List[User], group_id: UUID) -> Group:
        group = await super().get(db_session, id=group_id)
        group.users.extend(users)        
        db_session.add(group)
        await db_session.commit()
        await db_session.refresh(group)
        return group

group = CRUDGroup(Group)
