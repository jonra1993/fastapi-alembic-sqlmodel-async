from typing import Optional
from app.schemas.hero_schema import IHeroCreate, IHeroUpdate
from datetime import datetime
from app.crud.base_crud import CRUDBase
from app.models.hero_model import Hero
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDHero(CRUDBase[Hero, IHeroCreate, IHeroUpdate]):
    async def get_heroe_by_name(
        self, *, name: str, db_session: Optional[AsyncSession] = None
    ) -> Hero:
        db_session = db_session or db.session
        heroe = await db_session.execute(
            select(Hero).where(Hero.name == name)
        )  # TODO add pg_trgm to better search
        return heroe.scalar_one_or_none()

    async def get_count_of_heroes(
        self,
        *,
        start_time: datetime,
        end_time: datetime,
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        db_session = db_session or db.session
        subquery = (
            select(Hero)
            .where(
                and_(
                    Hero.created_at > start_time,
                    Hero.created_at < end_time,
                )
            )
            .subquery()
        )
        query = select(func.count()).select_from(subquery)
        count = await db_session.execute(query)
        value = count.scalar_one_or_none()
        return value


hero = CRUDHero(Hero)
