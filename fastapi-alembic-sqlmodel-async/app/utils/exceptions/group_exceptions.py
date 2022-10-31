from typing import Any, Dict, Optional, Union
from uuid import UUID

from fastapi import HTTPException, status
from requests import head


class GroupNameNotFoundException(HTTPException):
    def __init__(
        self,
        group_name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if group_name:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the group named {group_name}.",
                headers=headers,
            )
        else:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group name not found.",
                headers=headers,
            )


class GroupIdNotFoundException(HTTPException):
    def __init__(
        self,
        group_id: Optional[Union[UUID, str]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if group_id:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the group with id {group_id}.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group id not found.",
            headers=headers,
        )


class GroupNameExistException(HTTPException):
    def __init__(
        self,
        group_name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if group_name:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The group name {group_name} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="The group name already exists.",
            headers=headers,
        ) 