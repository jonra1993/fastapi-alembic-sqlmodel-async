from app.models.base_uuid_model import BaseUUIDModel
from sqlmodel import SQLModel


class MediaBase(SQLModel):
    title: str | None
    description: str | None
    path: str | None


class Media(BaseUUIDModel, MediaBase, table=True):
    pass
