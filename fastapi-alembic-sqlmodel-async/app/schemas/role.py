from typing import List
from app.models.role import RoleBase

class IRoleCreate(RoleBase):
    pass

class IRoleRead(RoleBase):
    id: int

class IRoleReadWithRoles(RoleBase):
    pass
    #roles: List[IUserRead]

class IRoleUpdate(RoleBase):
    pass
