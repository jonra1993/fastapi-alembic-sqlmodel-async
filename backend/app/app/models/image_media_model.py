from .media_model import Media
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship


class ImageMediaBase(SQLModel):
    file_format: str | None = None
    width: int | None = None
    height: int | None = None


class ImageMedia(BaseUUIDModel, ImageMediaBase, table=True):
    media_id: UUID | None = Field(default=None, foreign_key="Media.id")
    media: Media = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "ImageMedia.media_id==Media.id",
        }
    )
