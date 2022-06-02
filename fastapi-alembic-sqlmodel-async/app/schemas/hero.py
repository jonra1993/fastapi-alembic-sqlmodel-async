from typing import Optional
from app.models.hero import HeroBase
from app.models.team import TeamBase
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
    team: Optional[TeamBase] = None

    