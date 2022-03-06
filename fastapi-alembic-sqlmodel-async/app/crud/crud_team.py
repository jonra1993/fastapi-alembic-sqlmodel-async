from app.schemas.hero_team import ITeamCreate, ITeamUpdate
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.hero_team import Team
from datetime import datetime

class CRUDTeam(CRUDBase[Team, ITeamCreate, ITeamUpdate]):
    async def get(self, db_session: AsyncSession, id: int) -> Team:    
        return await super().get(db_session, id)

    async def create(self, db_session: AsyncSession, *, obj_in: ITeamCreate) -> Team:        
        db_obj = Team.from_orm(obj_in)
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

team = CRUDTeam(Team)
