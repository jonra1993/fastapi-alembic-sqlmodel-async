from typing import Any, Dict, Optional, Union
from uuid import UUID

from fastapi import HTTPException, status
from requests import head


class RoleNameNotFoundException(HTTPException):
    def __init__(
        self,
        role_name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if role_name:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the role named {role_name}.",
                headers=headers,
            )
        else:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role name not found.",
                headers=headers,
            )


class RoleIdNotFoundException(HTTPException):
    def __init__(
        self,
        role_id: Optional[Union[UUID, str]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if role_id:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the role with id {role_id}.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role id not found.",
            headers=headers,
        )


class RoleNameExistException(HTTPException):
    def __init__(
        self,
        role_name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if role_name:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The role name {role_name} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="The role name already exists.",
            headers=headers,
        ) 