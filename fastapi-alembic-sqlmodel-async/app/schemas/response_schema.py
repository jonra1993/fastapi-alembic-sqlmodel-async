import math
from typing import Any, Dict, Generic, Sequence, Union, Optional, TypeVar
from fastapi_pagination import Params, Page
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic.generics import GenericModel
DataType = TypeVar("DataType")
T = TypeVar("T")


class PageBase(Page[T], Generic[T]):
    pages: int
    next_page: Optional[int]
    previous_page: Optional[int]


class IResponseBase(GenericModel, Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: Optional[T]


class IResponsePage(AbstractPage[T], Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: PageBase[T]

    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> Union[PageBase[T], None]:
        pages = math.ceil(total / params.size)
        return cls(
            data=PageBase(
                items=items,
                page=params.page,
                size=params.size,
                total=total,
                pages=pages,
                next_page=params.page + 1 if params.page < pages else None,
                previous_page=params.page - 1 if params.page > 1 else None,
            )
        )


class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"

class IGetResponsePaginated(IResponsePage[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data created correctly"


class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"


class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"


def create_response(
    data: Optional[DataType],
    message: Optional[str] = "",
    meta: Optional[Union[Dict, Any]] = {},
) -> Union[Dict[str, DataType], DataType]:
    if isinstance(data, IResponsePage):
        data.message = "Data paginated correctly" if not message else message
        data.meta = meta
        return data
    body_response = {"data": data, "message": message, "meta": meta}
    # It returns a dictionary to avoid doble validation https://github.com/tiangolo/fastapi/issues/3021
    return dict((k, v) for k, v in body_response.items() if v is not None)