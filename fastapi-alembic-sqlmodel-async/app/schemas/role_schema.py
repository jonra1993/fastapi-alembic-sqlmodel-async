from enum import Enum
from app.models.role_model import RoleBase
from uuid import UUID

class IRoleCreate(RoleBase):
    pass

class IRoleUpdate(RoleBase):
    pass

class IRoleRead(RoleBase):    
    id: UUID

class IRoleEnum(str, Enum):
    admin = 'admin'
    manager = 'manager'
    user = 'user'    