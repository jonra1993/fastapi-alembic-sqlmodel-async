from enum import Enum
from app.models.role_model import RoleBase
from uuid import UUID

class IRoleCreate(RoleBase):
    pass

class IRoleRead(RoleBase):
    id: UUID

class IRoleReadWithRoles(RoleBase):
    pass
    #roles: List[IUserRead]

class IRoleUpdate(RoleBase):
    pass

class IRoleEnum(str, Enum):
    admin = 'admin'
    manager = 'manager'
    user = 'user'    