from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from typing import List
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID

class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str

class Team(BaseUUIDModel, TeamBase, table=True):    
    heroes: List["Hero"] = Relationship(back_populates="team", sa_relationship_kwargs={"lazy": "selectin"})
    created_by_id: Optional[UUID] = Field(default=None, foreign_key="User.id")
    created_by: "User" = Relationship(sa_relationship_kwargs={"lazy":"selectin", "primaryjoin":"Team.created_by_id==User.id"})