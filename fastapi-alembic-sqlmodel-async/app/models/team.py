from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str

class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    heroes: List["Hero"] = Relationship(back_populates="team", sa_relationship_kwargs={"lazy": "selectin"})
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_by: "User" = Relationship(sa_relationship_kwargs={"lazy":"selectin", "primaryjoin":"Team.created_by_id==User.id"})