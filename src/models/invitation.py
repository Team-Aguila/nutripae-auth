from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base

# Tabla de asociación Invitation-Role
invitation_roles = Table(
    "invitation_roles",
    Base.metadata,
    Column("invitation_id", Integer, ForeignKey("invitations.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    email = Column(String(150), nullable=False)
    status_id = Column(Integer, ForeignKey("invitation_statuses.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = relationship("InvitationStatus")
    created_by = relationship("User")
    roles = relationship("Role", secondary=invitation_roles)