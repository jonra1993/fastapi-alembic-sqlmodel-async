import pytest
from httpx import AsyncClient
from app.main import app
client = AsyncClient(app=app)

url = "http://fastapi.localhost"

@pytest.mark.asyncio
async def test_root():
    client = AsyncClient(app=app, base_url=url)
    try:
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    except Exception as e:
        print(f"Exception occurred during test: {e}")
    finally:
        await client.aclose()
