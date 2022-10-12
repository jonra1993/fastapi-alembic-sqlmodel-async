from typing import List
from pydantic import BaseModel
from app.schemas.role_schema import IRoleRead
from enum import Enum

class IMetaGeneral(BaseModel):
    roles: List[IRoleRead]


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"