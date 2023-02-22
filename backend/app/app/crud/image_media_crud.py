from app.crud.base_crud import CRUDBase
from app.models.image_media_model import ImageMedia
from app.schemas.image_media_schema import IImageMediaCreate, IImageMediaUpdate


class CRUDImageMedia(CRUDBase[ImageMedia, IImageMediaCreate, IImageMediaUpdate]):
    pass


image = CRUDImageMedia(ImageMedia)
