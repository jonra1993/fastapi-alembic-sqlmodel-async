from app.models.group import Group
from app.models.user import User
from app.schemas.group import IGroupCreate, IGroupUpdate
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession

class CRUDGroup(CRUDBase[Group, IGroupCreate, IGroupUpdate]):
    async def add_user_to_group(self, db_session: AsyncSession, *, user: User, group_id) -> Group:
        group = await super().get(db_session, group_id)
        group.users.append(user)        
        db_session.add(group)
        await db_session.commit()
        await db_session.refresh(group)
        return group

group = CRUDGroup(Group)
