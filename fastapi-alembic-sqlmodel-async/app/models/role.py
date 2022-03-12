from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional

class RoleBase(SQLModel):
    name: str
    description: str

class Role(RoleBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    users: List["User"] = Relationship(back_populates="role")


