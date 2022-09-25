from typing import Optional
from app.models.hero_model import HeroBase
from app.models.team_model import TeamBase
from uuid import UUID

class IHeroCreate(HeroBase):
    pass

class IHeroRead(HeroBase):
    id: UUID

class IHeroUpdate(HeroBase):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[UUID] = None

class IHeroReadWithTeam(IHeroRead):
    team: TeamBase

    