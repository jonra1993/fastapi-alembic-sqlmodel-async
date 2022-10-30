from typing import Any, Dict, Optional, Union
from uuid import UUID

from fastapi import HTTPException, status
from requests import head


class TeamIdNotFoundException(HTTPException):
    def __init__(
        self,
        team_id: Optional[Union[UUID, str]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if team_id:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the team with id {team_id}.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team id not found.",
            headers=headers,
        )


class TeamNameExistException(HTTPException):
    def __init__(
        self,
        team_name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if team_name:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The team name {team_name} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="The team name already exists.",
            headers=headers,
        )
