from uuid import UUID
from app.utils.uuid6 import uuid7
from pydantic import BaseModel, validator
from enum import Enum
from app.schemas.role_schema import IRoleRead


class IGenderEnum(str, Enum):
    female = "female"
    male = "male"
    other = "other"


class IMetaGeneral(BaseModel):
    roles: list[IRoleRead]


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class IUserMessage(BaseModel):
    """User message schema."""

    user_id: UUID | None
    message: str


class IChatResponse(BaseModel):
    """Chat response schema."""

    id: str
    message_id: str
    sender: str
    message: str
    type: str

    @validator("id", "message_id", pre=True, allow_reuse=True)
    def check_ids(cls, v):
        if v == "" or v is None:
            return str(uuid7())
        return v

    @validator("sender")
    def sender_must_be_bot_or_you(cls, v):
        if v not in ["bot", "you"]:
            raise ValueError("sender must be bot or you")
        return v

    @validator("type")
    def validate_message_type(cls, v):
        if v not in ["start", "stream", "end", "error", "info"]:
            raise ValueError("type must be start, stream or end")
        return v
