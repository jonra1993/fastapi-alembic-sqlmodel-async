from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import SessionLocal
from sqlmodel import text
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
import aioredis

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.ASYNC_DATABASE_URI,
        engine_args={
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": settings.POOL_SIZE,
        "max_overflow": 64,
    }
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
        return await session.execute(query)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def on_startup():
    await add_postgresql_extension()
    redis =  aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    print('startup fastapi')    

app.include_router(api_router, prefix=settings.API_V1_STR)

