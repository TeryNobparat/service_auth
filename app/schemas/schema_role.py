from pydantic import BaseModel
from uuid import UUID
from typing import List


class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: UUID
    permissions: List[UUID] = []
    pages: List[UUID] = []
    
    class Config:
        from_attributes = True


class RoleUser(BaseModel):
    user_id : UUID
    role_id : UUID

class RoleUserCreate(RoleUser):
    pass

class RoleUserRead(RoleUser):
    id: UUID

    class Config:
        from_attributes = True




class UserOut(BaseModel):
    id: UUID
    username: str
    roles: list[RoleBase]

    class Config:
        from_attributes = True

