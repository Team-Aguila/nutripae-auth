from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class UserStatus(Base):
    __tablename__ = "user_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., ACTIVE, INACTIVE, DELETED

class ApiVersions(Base):
    __tablename__ = "api_versions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., v1, v2, v3

class HttpMethods(Base):
    __tablename__ = "http_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., GET, POST, PUT, DELETE

class Modules(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., auth, user, project

class Features(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., auth, user, project

class ModulesFeatures(Base):
    __tablename__ = "modules_features"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    feature_id = Column(Integer, ForeignKey("features.id"), nullable=False)

    module = relationship("Modules")
    feature = relationship("Features")

class InvitationStatus(Base):
    __tablename__ = "invitation_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., PENDING, ACCEPTED, EXPIRED, CANCELLED