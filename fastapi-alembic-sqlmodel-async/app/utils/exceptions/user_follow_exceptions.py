from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class UserNotFollowedException(HTTPException):
    def __init__(
        self,
        user_name: Optional[str] = None,
        target_user_name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if user_name and target_user_name:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{user_name} not following {target_user_name}.",
                headers=headers,
            )
            return

        if user_name:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{user_name} not following you.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not followed you.",
            headers=headers,
        )


class UserFollowedException(HTTPException):
    def __init__(
        self,
        target_user_name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if target_user_name:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{target_user_name} has been followed.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has been followed.",
            headers=headers,
        )


class SelfFollowedException(HTTPException):
    def __init__(
        self,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Following/Unfollowing self not allowed!",
            headers=headers,
        )
