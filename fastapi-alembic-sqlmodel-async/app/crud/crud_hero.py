from app.schemas.hero import IHeroCreate, IHeroUpdate
from app.crud.base_sqlmodel import CRUDBase
from app.models.hero import Hero

class CRUDHero(CRUDBase[Hero, IHeroCreate, IHeroUpdate]):
    pass

hero = CRUDHero(Hero)
