from typing import Any, Dict, Optional, Union
from uuid import UUID

from fastapi import HTTPException, status
from requests import head


class HeroNameNotFoundException(HTTPException):
    def __init__(
        self,
        hero_name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if hero_name:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the hero named {hero_name}.",
                headers=headers,
            )
        else:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hero name not found.",
                headers=headers,
            )


class HeroIdNotFoundException(HTTPException):
    def __init__(
        self,
        hero_id: Optional[Union[UUID, str]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if hero_id:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the hero with id {hero_id}.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero id not found.",
            headers=headers,
        )


class HeroNameExistException(HTTPException):
    def __init__(
        self,
        hero_name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if hero_name:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The hero name {hero_name} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="The hero name already exists.",
            headers=headers,
        ) 