from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.orm import relationship
import uuid

class PageRole(Base):
    __tablename__ = "page_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id"),nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"),nullable=False)

    role = relationship("Role", backref="page_roles", overlaps="roles,pages")
