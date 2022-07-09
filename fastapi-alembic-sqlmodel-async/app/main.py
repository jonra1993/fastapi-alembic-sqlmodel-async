from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import SessionLocal
from sqlmodel import text

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

async def add_postgresql_extension() -> None:
    async with SessionLocal() as session:
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        await session.execute(query)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def on_startup():
    await add_postgresql_extension()
    print('startup fastapi')    

app.include_router(api_router, prefix=settings.API_V1_STR)

