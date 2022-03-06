from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app.core.config import settings
from app.schemas.user import IUserCreate

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db_session: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    
    user_ = await crud.user.get_by_email(db_session, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user_:
        user_in = IUserCreate(
            first_name = "Admin",
            last_name = "Admin",
            password = settings.FIRST_SUPERUSER_PASSWORD,
            email = settings.FIRST_SUPERUSER_EMAIL,
            is_superuser=True,                     
        )
        await crud.user.create(db_session, obj_in = user_in)  # noqa: F841