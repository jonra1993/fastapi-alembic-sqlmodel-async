from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app.schemas.role import IRoleCreate
from app.core.config import settings
from app.schemas.user import IUserCreate

roles = [
    {
        "name": "admin",
        "description": "This the Admin role"
    },
    {
        "name": "manager",
        "description": "Manager role"
    },
    {
        "name": "user",
        "description": "User role"
    },
]

users = [
    {
        "first_name":"Admin",
        "last_name":"FastAPI",
        "password":settings.FIRST_SUPERUSER_PASSWORD,
        "email":settings.FIRST_SUPERUSER_EMAIL,
        "is_superuser": True,
        "role":"admin"
    }         
]

async def init_db(db_session: AsyncSession) -> None:

    for role in roles:
        role_current = await crud.role.get_role_by_name(db_session, name=role["name"])
        if not role_current:
            role_in = IRoleCreate(name=role["name"], description=role["description"])
            await crud.role.create(db_session, obj_in=role_in)

    
    for user in users:
        current_user = await crud.user.get_by_email(db_session, email=user["email"])
        role = await crud.role.get_role_by_name(db_session, name=user["role"])
        if not current_user:
            user_in = IUserCreate(
                first_name=user["first_name"],
                last_name=user["last_name"],
                password=user["password"],
                email=user["email"],
                is_superuser=user["is_superuser"],
                role_id=role.id
            )
            await crud.user.create(db_session, obj_in=user_in)
