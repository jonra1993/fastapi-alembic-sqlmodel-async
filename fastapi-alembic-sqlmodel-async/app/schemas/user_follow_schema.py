from app.models.user_follow_model import UserFollowBase
from app.utils.partial import optional


class IUserFollowCreate(UserFollowBase):
    pass


# All these fields are optional
@optional
class IUserFollowUpdate(UserFollowBase):
    pass


class IUserFollowRead(UserFollowBase):
    is_mutual: bool
