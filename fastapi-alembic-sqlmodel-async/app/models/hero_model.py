from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_id: Optional[UUID] = Field(default=None, foreign_key="Team.id")

class Hero(BaseUUIDModel, HeroBase, table=True):    
    team: Optional["Team"] = Relationship(back_populates="heroes", sa_relationship_kwargs={"lazy": "selectin"})
    created_by_id: Optional[UUID] = Field(default=None, foreign_key="User.id")
    created_by: "User" = Relationship(sa_relationship_kwargs={"lazy":"selectin", "primaryjoin":"Hero.created_by_id==User.id"})
    