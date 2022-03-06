from fastapi import APIRouter
from app.api.api_v1.endpoints import user, hero, team, song, login_form
api_router = APIRouter()
api_router.include_router(login_form.router, tags=['login_form'])
api_router.include_router(user.router, tags=['user'])
api_router.include_router(team.router, tags=['team'])
api_router.include_router(hero.router, tags=['hero'])
api_router.include_router(song.router, tags=['song'])
