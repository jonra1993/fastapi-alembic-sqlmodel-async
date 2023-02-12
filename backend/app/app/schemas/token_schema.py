from pydantic import BaseModel
from .user_schema import IUserRead


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
