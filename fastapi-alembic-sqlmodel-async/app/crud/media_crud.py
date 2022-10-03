from app.crud.base_crud import CRUDBase
from app.models.media_model import ImageMedia
from app.schemas.media_schema import IImageMediaCreate, IImageMediaUpdate


class CRUDImageMedia(CRUDBase[ImageMedia, IImageMediaCreate, IImageMediaUpdate]):
    pass


image = CRUDImageMedia(ImageMedia)
