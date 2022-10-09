from typing import List, Optional
from app.models.group_model import GroupBase
from .user_schema import IUserReadWithoutGroups
from uuid import UUID

class IGroupCreate(GroupBase):
    pass

class IGroupRead(GroupBase):
    id: UUID

class IGroupReadWithUsers(GroupBase):
    id: UUID
    users: Optional[List[IUserReadWithoutGroups]] = []

class IGroupUpdate(GroupBase):
    pass
