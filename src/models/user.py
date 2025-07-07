from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from models.role import user_roles  # Import from the new location

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String(20), nullable=True)
    status_id = Column(Integer, ForeignKey("user_statuses.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    status = relationship("UserStatus")
    project = relationship("Project", back_populates="users")
    roles = relationship("Role", secondary=user_roles, back_populates="users")
