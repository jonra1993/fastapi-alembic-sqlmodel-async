from app.schemas.team import ITeamCreate, ITeamUpdate
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.team import Team
from datetime import datetime

class CRUDTeam(CRUDBase[Team, ITeamCreate, ITeamUpdate]):
    async def create_team(self, db_session: AsyncSession, *, obj_in: ITeamCreate, user_id: int) -> Team:        
        db_obj = Team.from_orm(obj_in)
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()
        db_obj.created_by_id = user_id   
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

team = CRUDTeam(Team)
