from app.schemas.hero import IHeroCreate, IHeroUpdate
from app.crud.base_sqlmodel import CRUDBase
from app.models.hero import Hero
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

class CRUDHero(CRUDBase[Hero, IHeroCreate, IHeroUpdate]):
    async def get_heroe_by_name(self, db_session: AsyncSession, *, name: str) -> Hero:
        heroe = await db_session.exec(select(Hero).where(Hero.name == name))
        return heroe.first()

hero = CRUDHero(Hero)
