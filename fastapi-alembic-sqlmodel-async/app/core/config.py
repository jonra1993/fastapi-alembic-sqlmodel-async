import os
from pydantic import BaseSettings, PostgresDsn, validator, EmailStr, AnyHttpUrl
from typing import Optional, Dict, Any, Union, List
import secrets

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = os.environ["PROJECT_NAME"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DATABASE_USER: str = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD")
    DATABASE_HOST: str = os.environ.get("DATABASE_HOST")
    DATABASE_PORT: Union[int, str] = os.environ.get("DATABASE_PORT")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME")
    ASYNC_DATABASE_URI: Optional[
        Any
    ] = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    @validator("ASYNC_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=values.get("DATABASE_PORT"),
            path=f"/{values.get('DATABASE_NAME') or ''}",
        )

    FIRST_SUPERUSER_EMAIL: EmailStr = os.environ.get("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD: str = os.environ.get("FIRST_SUPERUSER_PASSWORD")
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENCRYPT_KEY = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: Union[List[str], List[AnyHttpUrl]] = os.environ[
        "BACKEND_CORS_ORIGINS"
    ]
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")

settings = Settings()
