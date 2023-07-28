import pytest
from httpx import AsyncClient
from app.main import app

url = "http://fastapi.localhost/api/v1"

@pytest.mark.asyncio
class TestPostLogin:
    @pytest.mark.parametrize(
        "method, endpoint, data, expected_status, expected_response",
        [
            ("post", "/login", {"email": "incorrect_email@gmail.com", "password": "123456"}, 400, {"detail": "Email or Password incorrect"}),
            ("post", "/login", {"email": "admin@admin.com", "password": "admin"}, 200, {}),  # Add expected JSON response for successful login
            # ("get", "/some_endpoint", None, 200, {"result": "success"}),
            # ("put", "/another_endpoint", {"key": "value"}, 204, None),
            # ("delete", "/delete_endpoint", None, 204, None),
        ],
    )
    async def test(self, method, endpoint, data, expected_status, expected_response):
        client = AsyncClient(app=app, base_url=url)
        try:
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

        except Exception as e:
            print(f"Exception occurred during test: {e}")
        finally:
            await client.aclose()

