from typing import Any, Dict, Optional, Union
from uuid import UUID

from fastapi import HTTPException, status
from requests import head


class ContentNoChangeException(HTTPException):
    def __init__(
        self,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers
        )
