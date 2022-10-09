from app.models.user_model import UserBase
from .media_schema import IImageMediaRead
from .role_schema import IRoleRead
from typing import Optional, List
from uuid import UUID
from enum import Enum


class IUserCreate(UserBase):    
    password: Optional[str]

class IUserUpdate(UserBase):
    pass

class IUserRead(UserBase):
    id: UUID
    role: Optional[IRoleRead] = None
    groups: List["IGroupRead"] = []
    image: Optional[IImageMediaRead]

class IUserReadWithoutGroups(UserBase):
    id: UUID
    role: Optional[IRoleRead] = None
    image: Optional[IImageMediaRead]

class IUserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
