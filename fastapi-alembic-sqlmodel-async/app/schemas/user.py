from app.models.user import User
from pydantic import BaseModel, EmailStr
from typing import Optional

class IUserCreate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    password : Optional[str]
    email: EmailStr
    is_superuser: bool = False
        
class IUserResponse(User):
    class Config:
        fields = {
            'hashed_password': {'exclude': True},
        }

class IUserRead(IUserResponse):
    pass      

class IUserUpdate(BaseModel):
    id : int
    email : EmailStr
    is_active : bool = True
