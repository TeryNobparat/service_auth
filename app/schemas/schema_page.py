from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

# Base schema สำหรับการสร้าง / แก้ไขหน้า
class PageBase(BaseModel):
    title: str
    path: str
    icon: Optional[str] = None
    parent_id: Optional[UUID] = None
    order_index: Optional[int] = 0
    is_active: Optional[bool] = True

# สำหรับใช้ตอน create
class PageCreate(PageBase):
    pass

# สำหรับใช้ตอน update
class PageUpdate(PageBase):
    pass

# สำหรับใช้ตอนอ่านข้อมูล
class PageRead(PageBase):
    id: UUID
    children: Optional[List["PageRead"]] = []

    class Config:
        from_attributes = True


class RolePageUpdate(BaseModel):
    role_id: List[UUID]









