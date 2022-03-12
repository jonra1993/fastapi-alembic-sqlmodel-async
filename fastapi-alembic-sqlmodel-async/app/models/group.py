from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from .links import LinkGroupUser

class GroupBase(SQLModel):
    name: str
    description: str

class Group(GroupBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_by: "User" = Relationship(sa_relationship_kwargs={"lazy":"selectin", "primaryjoin":"Group.created_by_id==User.id"})    
    users: List["User"] = Relationship(back_populates="groups", link_model=LinkGroupUser)




