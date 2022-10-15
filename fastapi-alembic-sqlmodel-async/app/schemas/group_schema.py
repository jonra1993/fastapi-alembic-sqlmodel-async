from typing import List, Optional
from app.models.group_model import GroupBase
from app.utils.partial import optional
from .user_schema import IUserReadWithoutGroups
from uuid import UUID

class IGroupCreate(GroupBase):
    pass

class IGroupRead(GroupBase):
    id: UUID

class IGroupReadWithUsers(GroupBase):
    id: UUID
    users: Optional[List[IUserReadWithoutGroups]] = []

#All these fields are optional
@optional
class IGroupUpdate(GroupBase):
    pass
