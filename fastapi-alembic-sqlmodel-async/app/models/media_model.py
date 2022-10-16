from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


class MediaBase(SQLModel):
    title: Optional[str]
    description: Optional[str]
    path: Optional[str]


class Media(BaseUUIDModel, MediaBase, table=True):
    pass


class ImageMediaBase(SQLModel):
    file_format: Optional[str]
    width: Optional[int]
    height: Optional[int]


class ImageMedia(BaseUUIDModel, ImageMediaBase, table=True):
    media_id: Optional[UUID] = Field(default=None, foreign_key="Media.id")
    media: Media = Relationship(
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "ImageMedia.media_id==Media.id",
        }
    )
