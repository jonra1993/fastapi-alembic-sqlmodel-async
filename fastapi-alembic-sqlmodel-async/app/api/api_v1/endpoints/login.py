from typing import Any
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api import deps
from app.core.config import settings
from app.schemas.token import OpenIDToken, RefreshToken
from app.schemas.common import IMetaGeneral, IPostResponseBase
from fastapi_keycloak import FastAPIKeycloak, UsernamePassword, OIDCUser, KeycloakUser
from app.utils.keycloak import get_auth_token, get_auth_token_from_refresh

router = APIRouter()

@router.post("/login/access-token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    idp: FastAPIKeycloak = Depends(deps.get_auth_session),
) -> OpenIDToken:
    token = await get_auth_token(
        form_data=form_data,
        client_id=settings.KEYCLOAK_CLIENT_ID,
        client_secret=settings.KEYCLOAK_CLIENT_SECRET,
        token_uri=idp.token_uri,
    )
    return token


@router.post("/login", response_model=IPostResponseBase[KeycloakUser])
async def login_backoffice(
    form: UsernamePassword = Body(...),
    db_session: AsyncSession = Depends(deps.get_db),
    meta_data: IMetaGeneral = Depends(deps.get_general_meta),
    idp: FastAPIKeycloak = Depends(deps.get_auth_session),
) -> Any:
    """
    Login for all user in the backoffice
    """
    token = idp.user_login(
        username=form.username, password=form.password.get_secret_value()
    )
    decoded_token = idp._decode_token(token=token.access_token, audience="account")
    user = OIDCUser.parse_obj(decoded_token)
    user_data = idp.get_user(user_id=user.sub)
    roles = idp.get_all_roles()
    return IPostResponseBase[KeycloakUser](
        meta={"roles": roles}, data=user_data, message="Login correctly"
    )
@router.post("/login/refresh_token", response_model=IPostResponseBase[OpenIDToken], status_code=201)
async def get_refresh_token(
    body: RefreshToken = Body(...),
    idp: FastAPIKeycloak = Depends(deps.get_auth_session),
) -> Any:
    """
    Get Refresh token
    """
    token = await get_auth_token_from_refresh(
        client_id=settings.KEYCLOAK_CLIENT_ID,
        client_secret=settings.KEYCLOAK_CLIENT_SECRET,
        refresh_token=body.refresh_token,
        token_uri=idp.token_uri,
    )
    return IPostResponseBase[OpenIDToken](data=token)