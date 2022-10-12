from typing import Any, Dict, Generic, Sequence, Union, Optional, TypeVar
from fastapi_pagination import Params, Page
from fastapi_pagination.bases import AbstractPage, AbstractParams

DataType = TypeVar("DataType")
T = TypeVar("T")


class IResponseBase(AbstractPage[T], Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: Union[Page[T], T]

    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> Union[Page[T], None]:
        if not items:
            return
        return cls(
            data=Page(items=items, page=params.page, size=params.size, total=total)
        )


class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data created correctly"


class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"


class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"


def create_response(
    data: Optional[DataType], message: Optional[str] = "", meta: Optional[Union[Dict, Any]] = {}
) -> Union[Dict[str, DataType], DataType]:
    if isinstance(data, IResponseBase):
        data.message = "Data paginated correctly" if not message else message
        data.meta = meta
        return data
    body_response = {"data": data, "message": message, "meta": meta}
    #It returns a dictionary to avoid doble validation https://github.com/tiangolo/fastapi/issues/3021
    return dict((k, v) for k, v in body_response.items() if v is not None)

