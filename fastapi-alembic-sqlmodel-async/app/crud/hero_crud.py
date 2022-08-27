from typing import Optional
from app.schemas.hero_schema import IHeroCreate, IHeroUpdate
from app.crud.base_crud import CRUDBase
from app.models.hero_model import Hero
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

class CRUDHero(CRUDBase[Hero, IHeroCreate, IHeroUpdate]):
    async def get_heroe_by_name(self, *, name: str, db_session: Optional[AsyncSession] = None) -> Hero:
        db_session = db_session or db.session
        heroe = await db_session.execute(select(Hero).where(Hero.name == name))
        return heroe.scalar_one_or_none()

hero = CRUDHero(Hero)
