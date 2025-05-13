from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class PageRole(Base):
    __tablename__ = "page_roles"

    page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
