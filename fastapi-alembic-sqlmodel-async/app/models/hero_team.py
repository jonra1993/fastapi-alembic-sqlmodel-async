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
    heroes: List["Hero"] = Relationship(back_populates="team")

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    team: Optional[Team] = Relationship(back_populates="heroes")
