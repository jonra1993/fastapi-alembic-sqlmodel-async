from fastapi import FastAPI
from app.api.deps import get_redis_client
from uuid import uuid4
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router as api_router_v1
from app.core.config import settings
from fastapi_async_sqlalchemy import db
from app.utils.uuid7 import uuid7 as _uuid7, uuid8
from uuid6 import uuid7
from sqlmodel import text
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
import timeit
from app.utils import snowflake

# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.ASYNC_DATABASE_URI,
    engine_args={
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": settings.POOL_SIZE,
        "max_overflow": 64,
    },
)

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def add_postgresql_extension() -> None:
    async with db():
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        return await db.session.execute(query)


class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)
        self.message = message


@app.get("/")
async def root():
    # define the code statement to test and
    # calculate the execution time

    # exec_uuid4_time = timeit.repeat(lambda:uuid4(), number = 10000, repeat=5)
    # for index, exec_time in enumerate(exec_uuid4_time, 1):
    #     m_secs = round(exec_time * 10 ** 2, 2)
    #     print(f"Case {index}: Time uuid4 Taken: {m_secs}µs")

    # print("#"*10)
    # exec_uuid7_time = timeit.repeat(lambda:uuid7(), number = 10000, repeat=5)
    # for index, exec_time in enumerate(exec_uuid7_time, 1):
    #     m_secs = round(exec_time * 10 ** 2, 2)
    #     print(f"Case {index}: Time uuid7 Taken: {m_secs}µs")
    
    # print("#"*10)
    # exec_uuid8_time = timeit.repeat(lambda:uuid8(), number = 10000, repeat=5)
    # for index, exec_time in enumerate(exec_uuid8_time, 1):
    #     m_secs = round(exec_time * 10 ** 2, 2)
    #     print(f"Case {index}: Time uuid8 Taken: {m_secs}µs")

    # print("#"*10)
    # exec_snowflake_time = timeit.repeat(lambda:snowflake.generator(), number = 10000, repeat=5)
    # # printing the execution time
    # for index, exec_time in enumerate(exec_snowflake_time, 1):
    #     # printing execution time of code in microseconds
    #     m_secs = round(exec_time * 10 ** 2, 2)
    #     print(f"Case {index}: Time snowflake Taken: {m_secs}µs")
    
    return {"message": "Hello World"}


@app.on_event("startup")
async def on_startup():
    await add_postgresql_extension()
    redis_client = await get_redis_client()
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    print("startup fastapi")


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)
add_pagination(app)
