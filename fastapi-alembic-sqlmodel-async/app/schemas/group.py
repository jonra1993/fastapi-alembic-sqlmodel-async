from typing import List
from app.models.group import GroupBase
from .user import IUserReadWithoutGroups

class IGroupCreate(GroupBase):
    pass

class IGroupRead(GroupBase):
    id: int

class IGroupReadWithUsers(GroupBase):
    id: int
    users: List[IUserReadWithoutGroups]

class IGroupUpdate(GroupBase):
    pass
