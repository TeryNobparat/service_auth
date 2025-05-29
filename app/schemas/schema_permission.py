from pydantic import BaseModel
from uuid import UUID
from typing import List

class PermissionBase(BaseModel):
    name: str

class PermissionCreate(PermissionBase):
    pass

class PermissionRead(PermissionBase):
    id: UUID

    class Config:
        from_attributes = True

class RolePermission(BaseModel):
    permission_id : UUID
    role_id : UUID

class RolePermissionCreate(RolePermission):
    pass

class RolePermissionRead(RolePermission):
    id: UUID

    class Config:
        from_attributes = True   


class RolePermissiononRead(BaseModel):
    name: str

    class Config:
        from_attributes = True   


