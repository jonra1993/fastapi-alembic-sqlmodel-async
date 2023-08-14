from app.models.hero_model import HeroBase
from app.models.team_model import TeamBase
from app.utils.partial import optional
from uuid import UUID
from pydantic import validator


class IHeroCreate(HeroBase):
    @validator("age", pre=True, check_fields=False, always=True)
    def check_age(cls, value, values, **kwargs) -> int:
        if value < 0:
            raise ValueError("Invalida age")
        return value


# All these fields are optional
@optional
class IHeroUpdate(HeroBase):
    pass


class IHeroRead(HeroBase):
    id: UUID


class IHeroReadWithTeam(IHeroRead):
    team: TeamBase | None
