from typing import Optional
from .user import IUserRead
from pydantic import BaseModel

class OpenIDToken(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str
    not_before_policy: Optional[int]
    session_state: str
    scope: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user: IUserRead

class TokenRead(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str
