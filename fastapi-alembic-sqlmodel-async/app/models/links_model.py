from sqlmodel import Field
from typing import Optional
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID

class LinkGroupUser(BaseUUIDModel, table=True):
    group_id: Optional[UUID] = Field(default=None, nullable=False, foreign_key="Group.id", primary_key=True)
    user_id: Optional[UUID] = Field(default=None, nullable=False, foreign_key="User.id", primary_key=True)
