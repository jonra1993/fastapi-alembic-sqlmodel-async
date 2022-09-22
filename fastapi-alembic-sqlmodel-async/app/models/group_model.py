from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from .links_model import LinkGroupUser
from app.models.base_uuid_model import BaseUUIDModel
from app.models.user_model import User
from uuid import UUID

class GroupBase(SQLModel):
    name: str
    description: str

class Group(BaseUUIDModel, GroupBase, table=True):    
    created_by_id: Optional[UUID] = Field(default=None, foreign_key="User.id")
    created_by: "User" = Relationship(sa_relationship_kwargs={"lazy":"selectin", "primaryjoin":"Group.created_by_id==User.id"})    
    users: List["User"] = Relationship(back_populates="groups", link_model=LinkGroupUser, sa_relationship_kwargs={"lazy": "selectin"})




