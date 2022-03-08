from app.crud.base_sqlmodel import CRUDBase
from app.models.song import Song
from app.schemas.song import ISongCreate, ISongUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

class CRUDSong(CRUDBase[Song, ISongCreate, ISongUpdate]):
    pass

song = CRUDSong(Song)
