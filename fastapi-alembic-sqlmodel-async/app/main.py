from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import SecretStr
from starlette.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.api.deps import get_auth_session
from fastapi_keycloak import KeycloakError

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


idp = get_auth_session()

idp.add_swagger_config(app)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.exception_handler(KeycloakError)
async def keycloak_exception_handler(request: Request, exc: KeycloakError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.reason},
    )

@app.post("/users2")
def create_user(first_name: str, last_name: str, email: str, password: SecretStr):
    return idp.create_user(first_name=first_name, last_name=last_name, username=email, email=email, password=password.get_secret_value(), send_email_verification=False)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def on_startup():
    print('startup fastapi')

app.include_router(api_router, prefix=settings.API_V1_STR)

