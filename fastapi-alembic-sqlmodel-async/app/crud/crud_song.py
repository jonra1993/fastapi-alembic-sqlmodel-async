from app.crud.base_sqlmodel import CRUDBase
from app.models.song import Song
from app.schemas.song import ISongCreate, ISongUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

class CRUDSong(CRUDBase[Song, ISongCreate, ISongUpdate]):

    async def create(self, db_session: AsyncSession, *, obj_in: ISongCreate) -> Song:        
        db_obj = Song.from_orm(obj_in)
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

song = CRUDSong(Song)
