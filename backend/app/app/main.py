import gc
import logging
from contextlib import asynccontextmanager
from typing import Any
from uuid import UUID, uuid4

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import WebSocketRateLimiter
from fastapi_pagination import add_pagination
from jwt import DecodeError, ExpiredSignatureError, MissingRequiredClaimError
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from sqlalchemy.pool import NullPool, QueuePool
from starlette.middleware.cors import CORSMiddleware
from transformers import pipeline

from app import crud
from app.api.deps import get_redis_client
from app.api.v1.api import api_router as api_router_v1
from app.core.config import ModeEnum, settings
from app.core.security import decode_token
from app.schemas.common_schema import IChatResponse, IUserMessage
from app.utils.fastapi_globals import GlobalsMiddleware, g
from app.utils.uuid6 import uuid7


async def user_id_identifier(request: Request):
    if request.scope["type"] == "http":
        # Retrieve the Authorization header from the request
        auth_header = request.headers.get("Authorization")

        if auth_header is not None:
            # Check that the header is in the correct format
            header_parts = auth_header.split()
            if len(header_parts) == 2 and header_parts[0].lower() == "bearer":
                token = header_parts[1]
                try:
                    payload = decode_token(token)
                except ExpiredSignatureError:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Your token has expired. Please log in again.",
                    )
                except DecodeError:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Error when decoding the token. Please check your request.",
                    )
                except MissingRequiredClaimError:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="There is no required field in your token. Please contact the administrator.",
                    )

                user_id = payload["sub"]

                return user_id

    if request.scope["type"] == "websocket":
        return request.scope["path"]

    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]

    client = request.client
    ip = getattr(client, "host", "0.0.0.0")
    return ip + ":" + request.scope["path"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    redis_client = await get_redis_client()
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    await FastAPILimiter.init(redis_client, identifier=user_id_identifier)

    # Load a pre-trained sentiment analysis model as a dictionary to an easy cleanup
    models: dict[str, Any] = {
        "sentiment_model": pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        ),
    }
    g.set_default("sentiment_model", models["sentiment_model"])
    print("startup fastapi")
    yield
    # shutdown
    await FastAPICache.clear()
    await FastAPILimiter.close()
    models.clear()
    g.cleanup()
    gc.collect()


# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=str(settings.ASYNC_DATABASE_URI),
    engine_args={
        "echo": False,
        # "pool_pre_ping": True,
        # "pool_size": settings.POOL_SIZE,
        # "max_overflow": 64,
        "poolclass": NullPool
        if settings.MODE == ModeEnum.testing
        else QueuePool,  # Asincio pytest works with NullPool
    },
)
app.add_middleware(GlobalsMiddleware)

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(
        self,
        http_code: int = 500,
        code: str | None = None,
        message: str = "This is an error message",
    ):
        self.http_code = http_code
        self.code = code if code else str(self.http_code)
        self.message = message


@app.get("/")
async def root():
    """
    An example "Hello world" FastAPI route.
    """
    # if oso.is_allowed(user, "read", message):
    return {"message": "Hello World"}


@app.websocket("/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: UUID):
    session_id = str(uuid4())
    key: str = f"user_id:{user_id}:session:{session_id}"
    await websocket.accept()
    redis_client = await get_redis_client()
    ws_ratelimit = WebSocketRateLimiter(times=200, hours=24)
    chat = ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
    chat_history = []

    async with db():
        user = await crud.user.get_by_id_active(id=user_id)
        if user is not None:
            await redis_client.set(key, str(websocket))

    active_connection = await redis_client.get(key)
    if active_connection is None:
        await websocket.send_text(f"Error: User ID '{user_id}' not found or inactive.")
        await websocket.close()
    else:
        while True:
            try:
                # Receive and send back the client message
                data = await websocket.receive_json()
                await ws_ratelimit(websocket)
                user_message = IUserMessage.parse_obj(data)
                user_message.user_id = user_id

                resp = IChatResponse(
                    sender="you",
                    message=user_message.message,
                    type="stream",
                    message_id=str(uuid7()),
                    id=str(uuid7()),
                )
                await websocket.send_json(resp.dict())

                # # Construct a response
                start_resp = IChatResponse(
                    sender="bot", message="", type="start", message_id="", id=""
                )
                await websocket.send_json(start_resp.dict())

                result = chat([HumanMessage(content=resp.message)])
                chat_history.append((user_message.message, result.content))

                end_resp = IChatResponse(
                    sender="bot",
                    message=result.content,
                    type="end",
                    message_id=str(uuid7()),
                    id=str(uuid7()),
                )
                await websocket.send_json(end_resp.dict())
            except WebSocketDisconnect:
                logging.info("websocket disconnect")
                break
            except Exception as e:
                logging.error(e)
                resp = IChatResponse(
                    message_id="",
                    id="",
                    sender="bot",
                    message="Sorry, something went wrong. Your user limit of api usages has been reached.",
                    type="error",
                )
                await websocket.send_json(resp.dict())

        # Remove the live connection from Redis
        await redis_client.delete(key)


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)