from typing import Optional
from app.models.hero_model import HeroBase
from app.models.team_model import TeamBase
from uuid import UUID

class IHeroCreate(HeroBase):
    pass

class IHeroUpdate(HeroBase):
    name: Optional[str] = None  #This field is overrided
    secret_name: Optional[str] = None #This field is overrided

class IHeroRead(HeroBase):
    id: UUID

class IHeroReadWithTeam(IHeroRead):
    team: TeamBase

    