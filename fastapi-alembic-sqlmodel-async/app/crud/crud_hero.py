from typing import Optional
from app.schemas.hero_team import IHeroCreate, IHeroUpdate
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.hero_team import Hero
from datetime import datetime

class CRUDHero(CRUDBase[Hero, IHeroCreate, IHeroUpdate]):
    async def get_hero_by_id(self, db_session: AsyncSession, *, id: int) -> Optional[Hero]:
        #response = await db_session.exec(select(Hero).where(Hero.id == id).options(selectinload(Hero.team)))
        return await super().get(db_session, id)        

    async def create(self, db_session: AsyncSession, *, obj_in: IHeroCreate) -> Hero:        
        db_obj = Hero.from_orm(obj_in)
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

hero = CRUDHero(Hero)
