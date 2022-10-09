from pydantic import BaseModel, ValidationError, root_validator
from app.models.user_model import UserBase
from app.models.group_model import GroupBase
from .media_schema import IImageMediaRead
from .role_schema import IRoleRead
from typing import Optional, List
from uuid import UUID
from enum import Enum


class IUserCreate(UserBase):    
    password: Optional[str]
    class Config:
        hashed_password = 'Main'

class IUserUpdate(UserBase):
    pass

# This schema is used to avoid circular import
class IGroupReadBasic(GroupBase):
    id: UUID

class IUserRead(UserBase):
    id: UUID
    role: Optional[IRoleRead] = None
    groups: Optional[List[IGroupReadBasic]] = []
    image: Optional[IImageMediaRead]

class IUserReadWithoutGroups(UserBase):
    id: UUID
    role: Optional[IRoleRead] = None
    image: Optional[IImageMediaRead]

class IUserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
