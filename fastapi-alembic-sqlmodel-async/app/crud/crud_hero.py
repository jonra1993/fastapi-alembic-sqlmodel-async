from typing import Optional
from app.schemas.hero import IHeroCreate, IHeroUpdate
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.hero import Hero
from datetime import datetime

class CRUDHero(CRUDBase[Hero, IHeroCreate, IHeroUpdate]):
    async def create_hero(self, db_session: AsyncSession, *, obj_in: IHeroCreate, user_id: int) -> Hero:        
        db_obj = Hero.from_orm(obj_in)
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()
        db_obj.created_by_id = user_id   
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj


hero = CRUDHero(Hero)
