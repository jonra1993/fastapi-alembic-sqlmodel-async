from sqlmodel import SQLModel, Relationship
from typing import List
from app.models.base_uuid_model import BaseUUIDModel

class RoleBase(SQLModel):
    name: str
    description: str

class Role(BaseUUIDModel, RoleBase, table=True):    
    users: List["User"] = Relationship(back_populates="role", sa_relationship_kwargs={"lazy": "selectin"})


