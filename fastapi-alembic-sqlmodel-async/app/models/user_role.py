from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from pydantic import EmailStr

class RoleBase(SQLModel):
    name: str
    description: str

class Role(RoleBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    users: List["User"] = Relationship(back_populates="role", sa_relationship_kwargs={"lazy": "selectin"})

class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(nullable=True, index=True, sa_column_kwargs={"unique": True})    
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    birthdate: Optional[datetime]
    phone: Optional[str]
    state: Optional[str]
    country: Optional[str]
    address: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    hashed_password: str = Field(
        nullable=False, index=True
    )
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional[Role] = Relationship(back_populates="users", sa_relationship_kwargs={"lazy": "selectin"})
