from app.models.group_model import GroupBase
from app.utils.partial import optional
from uuid import UUID
from .user_schema import IUserReadWithoutGroups


class IGroupCreate(GroupBase):
    pass


class IGroupRead(GroupBase):
    id: UUID


class IGroupReadWithUsers(GroupBase):
    id: UUID
    users: list[IUserReadWithoutGroups] | None = []


# All these fields are optional
@optional
class IGroupUpdate(GroupBase):
    pass
