from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Page(Base):
    __tablename__ = "pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)               # ชื่อเมนูที่แสดงใน UI
    path = Column(String, nullable=False)                # เช่น "/users", "/dashboard"
    icon = Column(String, nullable=True)                 # เช่น "user", "settings"
    parent_id = Column(UUID(as_uuid=True), ForeignKey("pages.id"), nullable=True)
    order_index = Column(Integer, default=0)             # ลำดับเมนู
    is_active = Column(Boolean, default=True)            # สำหรับเปิด/ปิดเมนู

    # ความสัมพันธ์กับ Role
    roles = relationship("Role", secondary="page_roles", back_populates="pages")