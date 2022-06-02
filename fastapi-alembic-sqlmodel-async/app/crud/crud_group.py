from app.models.group import Group
from app.models.user import User
from app.schemas.group import IGroupCreate, IGroupUpdate
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from uuid import UUID

class CRUDGroup(CRUDBase[Group, IGroupCreate, IGroupUpdate]):
    async def create_group(self, db_session: AsyncSession, *, obj_in: IGroupCreate, user_id: UUID) -> Group:        
        db_obj = Group.from_orm(obj_in)
        db_obj.created_by_id = user_id
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def add_user_to_group(self, db_session: AsyncSession, *, user: User, group_id) -> Group:
        group = await super().get(db_session, group_id)
        group.users.append(user)        
        db_session.add(group)
        await db_session.commit()
        await db_session.refresh(group)
        return group

group = CRUDGroup(Group)
