import asyncio
import time
from uuid import UUID
from app import crud
from app.core.celery import celery
from app.models.hero_model import Hero
from app.schemas.hero_schema import IHeroCreate, IHeroRead, IHeroReadWithTeam
from app.db.session import SessionLocal
from asyncer import runnify

@celery.task(name="increment_a_value")
def increment(value: int) -> int:
    time.sleep(5)
    new_value = value + 1
    print("new_value", new_value)
    return new_value


async def get_hero(hero_id: UUID) -> Hero:
    async with SessionLocal() as session:
        await asyncio.sleep(5) # Add a delay of 5 seconds
        hero = await crud.hero.get(id=hero_id, db_session=session)
        return hero


@celery.task(name="print_hero")
def print_hero(hero_id: UUID) -> None:
    hero = runnify(get_hero)(hero_id=hero_id)
    print(f"hero_id {hero.id}") 
    return hero.id

