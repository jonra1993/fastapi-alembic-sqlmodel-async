from app.schemas.hero import IHeroCreate, IHeroUpdate
from app.crud.base_sqlmodel import CRUDBase
from app.models.hero import Hero
from fastapi_async_sqlalchemy import db
from sqlmodel import select

class CRUDHero(CRUDBase[Hero, IHeroCreate, IHeroUpdate]):
    async def get_heroe_by_name(self, *, name: str) -> Hero:
        heroe = await db.session.execute(select(Hero).where(Hero.name == name))
        return heroe.first()

hero = CRUDHero(Hero)
