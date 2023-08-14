import pytest
from httpx import AsyncClient
from typing import AsyncGenerator
from app.main import app
from app.core.config import settings

url = "http://fastapi.localhost/api/v1"

@pytest.fixture(scope='function')
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=url) as client:
        yield client

@pytest.mark.asyncio
class TestPostLogin:
    @pytest.mark.parametrize(
        "method, endpoint, data, expected_status, expected_response",
        [
            ("post", "/login", {"email": "incorrect_email@gmail.com", "password": "123456"}, 400, {"detail": "Email or Password incorrect"}),
            ("post", "/login", {"email": settings.FIRST_SUPERUSER_EMAIL, "password": settings.FIRST_SUPERUSER_PASSWORD}, 200, None),  # Add expected JSON response for successful login
            ("post", "/login/new_access_token", {"refresh_token": ""}, 403, {"detail": "Refresh token invalid"}),            
        ],
    )
    async def test(self, test_client, method, endpoint, data, expected_status, expected_response):
        async for client in test_client:        
            if method == "get":
                response = await client.get(endpoint)
            elif method == "put":
                response = await client.put(endpoint, json=data)
            elif method == "delete":
                response = await client.delete(endpoint)
            else:  # Default to POST
                response = await client.post(endpoint, json=data)

            assert response.status_code == expected_status
            if expected_response is not None:                
                assert response.json() == expected_response
