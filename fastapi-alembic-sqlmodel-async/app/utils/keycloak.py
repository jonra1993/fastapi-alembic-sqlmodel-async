from app.schemas.token import OpenIDToken
from fastapi.security import OAuth2PasswordRequestForm
import httpx
import json

async def get_auth_token(form_data = OAuth2PasswordRequestForm, client_id: str = '', client_secret: str = '', token_uri: str= '')-> OpenIDToken:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    request_body = {
        "username": form_data.username,
        "password": form_data.password,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "password",
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(token_uri, data=request_body, headers=headers)
        json_respose = json.loads(r.content)
        response = OpenIDToken.parse_obj(json.loads(r.content))
        response.not_before_policy = json_respose["not-before-policy"]
        return response
