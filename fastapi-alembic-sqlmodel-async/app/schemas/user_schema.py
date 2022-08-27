from app.models.user_model import UserBase
from app.models.group_model import GroupBase
from pydantic import BaseModel, EmailStr
from .role_schema import IRoleRead
from typing import Optional, List
from uuid import UUID
from enum import Enum

class IUserCreate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    password : Optional[str]
    email: EmailStr
    is_superuser: bool = False
    role_id: Optional[UUID]
        
class IUserReadWithoutGroups(UserBase):
    id: UUID
    role: Optional[IRoleRead] = None


class IGroupRead(GroupBase):
    id: UUID
    
class IUserRead(UserBase):
    id: UUID    
    role: Optional[IRoleRead] = None
    groups: List[IGroupRead] = []

class IUserUpdate(BaseModel):
    id : int
    email : EmailStr
    is_active : bool = True

class IUserStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'