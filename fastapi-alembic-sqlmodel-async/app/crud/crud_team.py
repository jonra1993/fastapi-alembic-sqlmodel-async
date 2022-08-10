from app.schemas.team import ITeamCreate, ITeamUpdate
from fastapi_async_sqlalchemy import db
from app.crud.base_sqlmodel import CRUDBase
from app.models.team import Team
from sqlmodel import select

class CRUDTeam(CRUDBase[Team, ITeamCreate, ITeamUpdate]):
    async def get_team_by_name(self, *, name: str) -> Team:
        team = await db.session.execute(select(Team).where(Team.name == name))
        return team.first()

team = CRUDTeam(Team)
