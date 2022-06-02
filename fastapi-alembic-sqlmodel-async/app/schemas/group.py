from typing import List
from app.models.group import GroupBase
from .user import IUserReadWithoutGroups
from uuid import UUID

class IGroupCreate(GroupBase):
    pass

class IGroupRead(GroupBase):
    id: UUID

class IGroupReadWithUsers(GroupBase):
    id: UUID
    users: List[IUserReadWithoutGroups]

class IGroupUpdate(GroupBase):
    pass
