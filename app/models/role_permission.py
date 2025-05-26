from sqlalchemy import Column,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True),ForeignKey("roles.id"), nullable=False)
    permission_id = Column(UUID(as_uuid=True),ForeignKey("permissions.id"), nullable=False)


    permission = relationship("Permission", backref="role_permissions", overlaps="roles,permissions")
