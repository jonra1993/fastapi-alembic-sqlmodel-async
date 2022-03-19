from ctypes import Union
from fastapi import status
from typing import Any, Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel
from app.schemas.role import IRoleRead

DataType = TypeVar("DataType")

class IResponseBase(GenericModel, Generic[DataType]):
    message: str = ""
    status: int = status.HTTP_200_OK
    meta: dict = {}
    data: Optional[DataType] = None

class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"

class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    status: int = status.HTTP_201_CREATED
    message: str = "Data created correctly"

class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"

class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"

class IMetaGeneral(BaseModel):
    roles: List[IRoleRead]