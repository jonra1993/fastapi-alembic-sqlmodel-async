from sqlmodel import Field
from typing import Optional
from app.models.base_uuid_model import BaseJoinUUIDModel
from uuid import UUID

class LinkGroupUser(BaseJoinUUIDModel, table=True):
    group_id: Optional[UUID] = Field(default=None, nullable=False, foreign_key="Group.id", primary_key=True)
    user_id: Optional[UUID] = Field(default=None, nullable=False, foreign_key="User.id", primary_key=True)
