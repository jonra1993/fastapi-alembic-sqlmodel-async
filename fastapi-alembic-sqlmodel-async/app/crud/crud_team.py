from app.schemas.team import ITeamCreate, ITeamUpdate
from app.crud.base_sqlmodel import CRUDBase
from app.models.team import Team

class CRUDTeam(CRUDBase[Team, ITeamCreate, ITeamUpdate]):
    pass

team = CRUDTeam(Team)
