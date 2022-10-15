from app.models.hero_model import HeroBase
from typing import List, Optional
from app.models.team_model import TeamBase
from app.utils.partial import optional
from uuid import UUID

class ITeamCreate(TeamBase):
    pass

#All these fields are optional
@optional
class ITeamUpdate(TeamBase):
    pass

class ITeamRead(TeamBase):
    id: UUID

class ITeamReadWithHeroes(ITeamRead):    
    heroes: List[HeroBase]
    