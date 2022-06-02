from fastapi_keycloak import FastAPIKeycloak
from app.core.config import settings

class AuthContextManager:
    def __init__(self):
        self.idp: FastAPIKeycloak = FastAPIKeycloak(
            server_url=settings.KEYCLOAK_SERVER,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            client_secret=settings.KEYCLOAK_CLIENT_SECRET,
            admin_client_secret=settings.KEYCLOAK_ADMIN_CLIENT_SECRET,
            realm=settings.KEYCLOAK_REALM,
            callback_uri=settings.KEYCLOAK_CALLBACK_URI,
        )

    def __enter__(self):
        return self.idp

    def __exit__(self, exc_type, exc_value, traceback):
        pass


