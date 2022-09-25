from typing import Dict, Generic, List, Optional, TypeVar, Union
from pydantic.generics import GenericModel
from pydantic import BaseModel, validator
from app.schemas.role_schema import IRoleRead
from enum import Enum

DataType = TypeVar("DataType")


class IResponseBase(GenericModel, Generic[DataType]):
    message: str = ""
    meta: dict = {}
    data: Optional[DataType] = None


class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data created correctly"


class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"


class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"


def create_response(
    data: Optional[DataType], message: Optional[str] = None, meta: Optional[dict] = None
) -> Dict[str, DataType]:
    body_response = {"data": data, "message": message, "meta": meta}
    return dict((k, v) for k, v in body_response.items() if v is not None)


class IMetaGeneral(BaseModel):
    roles: List[IRoleRead]


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"
