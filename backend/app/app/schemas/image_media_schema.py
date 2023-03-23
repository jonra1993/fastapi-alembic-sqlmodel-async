from app.models.image_media_model import ImageMediaBase
from .media_schema import IMediaRead
from app.utils.partial import optional


# Image Media
class IImageMediaCreate(ImageMediaBase):
    pass


# All these fields are optional
@optional
class IImageMediaUpdate(ImageMediaBase):
    pass


class IImageMediaRead(ImageMediaBase):
    media: IMediaRead | None
