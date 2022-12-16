from uuid import UUID
from app.models.user_follow_model import UserFollowBase
from app.utils.partial import optional
from pydantic import BaseModel


class IUserFollowCreate(UserFollowBase):
    pass


# All these fields are optional
@optional
class IUserFollowUpdate(UserFollowBase):
    pass


class IUserFollowRead(UserFollowBase):
    is_mutual: bool


class IUserFollowReadCommon(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    follower_count: int
    following_count: int
    is_mutual: bool
