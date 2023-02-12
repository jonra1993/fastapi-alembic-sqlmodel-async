import asyncio
import logging
from app.db.init_db import init_db
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_init_data() -> None:
    async with SessionLocal() as session:
        await init_db(session)


async def main() -> None:
    logger.info("Creating initial data")
    await create_init_data()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
