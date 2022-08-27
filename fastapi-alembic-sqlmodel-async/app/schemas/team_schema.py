from app.models.hero_model import HeroBase
from typing import List, Optional
from app.models.team_model import TeamBase
from pydantic import BaseModel
from uuid import UUID

class ITeamRead(TeamBase):
    id: UUID

class ITeamCreate(TeamBase):
    pass

class ITeamUpdate(BaseModel):
    name: Optional[str] = None
    headquarters: Optional[str] = None

class ITeamReadWithHeroes(ITeamRead):    
    heroes: List[HeroBase]
    