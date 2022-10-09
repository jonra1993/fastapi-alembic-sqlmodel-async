from typing import Optional
from app.utils.minio_client import MinioClient
from app.models.media_model import ImageMediaBase, MediaBase
from pydantic import validator
from app.core.config import settings
from app import api
from typing import Any, Optional, Union
from uuid import UUID

class IMediaCreate(MediaBase):
    pass

class IMediaUpdate(MediaBase):
    pass

class IMediaRead(MediaBase):
    id: Union[UUID, str]
    link: Optional[str] = None

    @validator(
        "link", pre=True, check_fields=False, always=True
    )  # Always true because link does not exist in the database
    def default_icon(cls, value: Any, values: Any) -> str:
        if values["path"] is None:
            return ""
        minio: MinioClient = api.deps.minio_auth()
        url = minio.presigned_get_object(
            bucket_name=settings.MINIO_BUCKET, object_name=values["path"]
        )
        return url

# Image Media
class IImageMediaCreate(ImageMediaBase):
    pass

class IImageMediaUpdate(ImageMediaBase):
    pass

class IImageMediaRead(ImageMediaBase):
    media: Optional[IMediaRead]