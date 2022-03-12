from typing import List, Optional
from app.models.hero import HeroBase

class IHeroCreate(HeroBase):
    pass

class IHeroRead(HeroBase):
    id: int

class IHeroUpdate(HeroBase):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None

class IHeroReadWithTeam(IHeroRead):
    team: Optional["ITeamRead"] = None

    