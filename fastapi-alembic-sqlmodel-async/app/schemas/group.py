from typing import List
from app.models.group import GroupBase
from .user import IUserReadWithoutGroups

class IGroupCreate(GroupBase):
    fleet_id: int

class IGroupRead(GroupBase):
    id: int

class IGroupReadWithUsers(GroupBase):
    users: List[IUserReadWithoutGroups]

class IGroupUpdate(GroupBase):
    pass
