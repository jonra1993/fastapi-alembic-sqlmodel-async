import pytest
from httpx import AsyncClient
from typing import AsyncGenerator
from app.main import app
client = AsyncClient(app=app)

url = "http://fastapi.localhost"

@pytest.fixture(scope='function')
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=url) as client:
        yield client

@pytest.mark.asyncio
async def test_root(test_client):
    async for client in test_client:      
        response = await client.get('/')
        assert response is not None
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
        await client.aclose()


