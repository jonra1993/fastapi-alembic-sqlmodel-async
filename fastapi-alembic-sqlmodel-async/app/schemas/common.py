from typing import Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel
from app.schemas.role import IRoleRead

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

class IMetaGeneral(BaseModel):
    roles: List[IRoleRead]