from typing import Optional
from app.models.hero_model import HeroBase
from app.models.team_model import TeamBase
from app.utils.partial import optional
from uuid import UUID

class IHeroCreate(HeroBase):
    pass

#All these fields are optional
@optional
class IHeroUpdate(HeroBase):
    pass

class IHeroRead(HeroBase):
    id: UUID

class IHeroReadWithTeam(IHeroRead):
    team: TeamBase

    