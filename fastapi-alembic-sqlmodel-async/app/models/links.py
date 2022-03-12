from sqlmodel import Field, SQLModel
from typing import Optional

class LinkGroupUser(SQLModel, table=True):
    group_id: Optional[int] = Field(default=None, nullable=False, foreign_key="group.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, nullable=False, foreign_key="user.id", primary_key=True)
