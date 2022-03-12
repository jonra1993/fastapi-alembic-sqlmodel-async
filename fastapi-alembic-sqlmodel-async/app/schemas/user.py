from app.models.user import UserBase
from app.models.group import GroupBase
from pydantic import BaseModel, EmailStr
from .role import IRoleRead
from typing import Optional, List

class IUserCreate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    password : Optional[str]
    email: EmailStr
    is_superuser: bool = False
    role_id: int
        
class IUserReadWithoutGroups(UserBase):
    id: int
    role: Optional[IRoleRead] = None


class IGroupRead(GroupBase):
    id: int
    
class IUserRead(UserBase):
    id: int    
    role: Optional[IRoleRead] = None
    groups: List[IGroupRead] = []

class IUserUpdate(BaseModel):
    id : int
    email : EmailStr
    is_active : bool = True
