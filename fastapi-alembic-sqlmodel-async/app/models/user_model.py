from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from app.models.links_model import LinkGroupUser
from typing import List, Optional
from pydantic import EmailStr
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID

class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(nullable=True, index=True, sa_column_kwargs={"unique": True})    
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    birthdate: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=True)) #birthday with timezone
    phone: Optional[str]
    state: Optional[str]
    country: Optional[str]
    address: Optional[str]    

class User(BaseUUIDModel, UserBase, table=True):    
    hashed_password: str = Field(
        nullable=False, index=True
    )
    role_id: Optional[UUID] = Field(default=None, foreign_key="Role.id")
    role: Optional["Role"] = Relationship(back_populates="users", sa_relationship_kwargs={"lazy": "selectin"})
    groups: List["Group"] = Relationship(back_populates="users", link_model=LinkGroupUser, sa_relationship_kwargs={"lazy": "selectin"})
