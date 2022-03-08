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

hero = CRUDHero(Hero)
