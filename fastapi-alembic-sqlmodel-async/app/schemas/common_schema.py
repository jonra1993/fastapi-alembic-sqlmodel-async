from typing import Dict, Generic, List, Optional, TypeVar, Union
from pydantic.generics import GenericModel
from fastapi_pagination import Page
from pydantic import BaseModel
from app.schemas.role_schema import IRoleRead
from enum import Enum

DataType = TypeVar("DataType")

class IResponseBase(GenericModel, Generic[DataType]):
    message: str = ""
    meta: Dict = {}
    data: Union[DataType, Page] = None

class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data created correctly"


class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"


class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"


def create_response(
    data: Union[DataType, Page], message: Optional[str] = None, meta: Optional[Dict] = None
) -> Dict[str, DataType]:
    new_data = dict(data) if isinstance(data, Page) else data
    body_response = {"data": new_data, "message": message, "meta": meta}
    return dict((k, v) for k, v in body_response.items() if v is not None)


class IMetaGeneral(BaseModel):
    roles: List[IRoleRead]


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"