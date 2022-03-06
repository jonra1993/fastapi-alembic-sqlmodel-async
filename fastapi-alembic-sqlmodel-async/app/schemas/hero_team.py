from typing import List, Optional
from app.models.hero_team import HeroBase, TeamBase
from sqlmodel import SQLModel

class IHeroCreate(HeroBase):
    pass

class IHeroRead(HeroBase):
    id: int

class IHeroUpdate(HeroBase):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None

class ITeamRead(TeamBase):
    id: int

class ITeamCreate(TeamBase):
    pass

class ITeamUpdate(SQLModel):
    name: Optional[str] = None
    headquarters: Optional[str] = None

class IHeroReadWithTeam(IHeroRead):
    team: Optional[ITeamRead] = None

class ITeamReadWithHeroes(ITeamRead):
    heroes: List[IHeroRead]
    