from typing import Any
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api import deps
from app.core.config import settings
from app.schemas.token import OpenIDToken
from app.schemas.common import IMetaGeneral, IPostResponseBase
from fastapi_keycloak import FastAPIKeycloak, UsernamePassword, OIDCUser, KeycloakUser
from app.utils.keycloak import get_auth_token

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
    print("token", token)
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
# @router.post("/login/refresh_token", response_model=IPostResponseBase[TokenRead], status_code=201)
# async def get_refresh_token(
#     body: RefreshToken = Body(...),
#     db_session: AsyncSession = Depends(deps.get_db),
# ) -> Any:
#     """
#     Get Refresh token
#     """
#     try:
#         payload = jwt.decode(body.refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(status_code=403,detail="Refresh token invalid")

#     if payload['type'] == 'refresh':
#         access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#         user = await crud.user.get(db_session, id=int(payload['sub']))
#         if user.is_active:
#             access_token = security.create_access_token( int(payload['sub']), expires_delta=access_token_expires)         
#             return IPostResponseBase[TokenRead](data=TokenRead(access_token=access_token,token_type= "bearer"), message="Access token generated correctly")
#         else:
#             raise HTTPException(status_code=404,detail="User inactive")
#     else:
#         raise HTTPException(status_code=404,detail="Incorrect token")

