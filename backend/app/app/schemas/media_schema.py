from app.utils.minio_client import MinioClient
from app.models.media_model import MediaBase
from pydantic import validator, AnyHttpUrl
from app.core.config import settings
from app.utils.partial import optional
from app import api
from typing import Any
from uuid import UUID


class IMediaCreate(MediaBase):
    pass


# All these fields are optional
@optional
class IMediaUpdate(MediaBase):
    pass


class IMediaRead(MediaBase):
    id: UUID | str
    link: str | None = None

    @validator(
        "link", pre=True, check_fields=False, always=True
    )  # Always true because link does not exist in the database
    def default_icon(cls, value: Any, values: Any) -> AnyHttpUrl:
        if values["path"] is None:
            return ""
        minio: MinioClient = api.deps.minio_auth()
        url = minio.presigned_get_object(
            bucket_name=settings.MINIO_BUCKET, object_name=values["path"]
        )
        return url
