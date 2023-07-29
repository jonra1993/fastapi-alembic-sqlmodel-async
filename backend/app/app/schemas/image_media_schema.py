from app.models.image_media_model import ImageMedia, ImageMediaBase
from app.models.media_model import Media
from pydantic import root_validator
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


class IImageMediaReadCombined(ImageMediaBase):
    link: str | None

    @root_validator(pre=True)
    def combine_attributes(cls, values):
        link_fields = {"link": values.get("link", None)}
        if "media" in values:
            if isinstance(values["media"], Media) and values["media"].path is not None:
                link_fields = {"link": values["media"].link}

        image_media_fields = {
            k: v for k, v in values.items() if k in ImageMedia.__fields__
        }
        output = {**image_media_fields, **link_fields}
        return output
