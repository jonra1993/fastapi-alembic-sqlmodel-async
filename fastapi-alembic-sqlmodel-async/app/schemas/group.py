from typing import List
from app.models.group import GroupBase
from app.schemas.user import IUserRead

class IGroupCreate(GroupBase):
    fleet_id: int

class IGroupRead(GroupBase):
    id: int

class IGroupReadWithUsers(GroupBase):
    users: List[IUserRead]

class IGroupUpdate(GroupBase):
    pass
