from app.models.hero_model import Hero
from app.models.user_model import User
from oso import Oso  # (1)


oso = Oso()  # (2)

# load policies
oso.register_class(Hero)
oso.register_class(User)

oso.load_files(["app/core/authz.polar"])


def is_authorized(actor: User, action: str, resource, **kwargs):
    return oso.is_allowed(actor=actor, action=action, resource=resource, **kwargs)
