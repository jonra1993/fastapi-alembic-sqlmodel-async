from typing import Optional
from .user import IUserResponse
from pydantic import BaseModel
from typing import Optional
        
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user: IUserResponse
    class Config:
        orm_mode : True


class TokenForm(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class TokenResponse(BaseModel):
    message: str
    status: int
    meta: Optional[dict]
    data: Token

    class Config:
        orm_mode : True