from typing import Optional
from app.schemas.hero import IHeroCreate, IHeroUpdate
from app.crud.base_sqlmodel import CRUDBase
from app.models.hero import Hero
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

class CRUDHero(CRUDBase[Hero, IHeroCreate, IHeroUpdate]):
    async def get_heroe_by_name(self, *, name: str, db_session: Optional[AsyncSession] = None) -> Hero:
        if db_session == None:
            db_session = db.session()
        heroe = await db_session.execute(select(Hero).where(Hero.name == name))
        return heroe.scalar_one_or_none()

hero = CRUDHero(Hero)
