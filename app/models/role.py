from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

    # ความสัมพันธ์กับ Page
    pages = relationship("Page", secondary="page_roles", back_populates="roles",overlaps="page_roles")

    # 🔧 แก้ชื่อ secondary และ back_populates ให้ตรงกับ user.py
    users = relationship("User", secondary="user_roles", back_populates="roles", overlaps="user_roles")

    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles", overlaps="role_permissions")
