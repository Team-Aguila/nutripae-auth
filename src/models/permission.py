from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import related models to make them available for relationship configuration
from models.base import Base
from models.role import role_permissions, Role
from models.parametric import ApiVersions, HttpMethods, ModulesFeatures


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String, unique=True, index=True, nullable=False
    ) 
    version_id = Column("version", Integer, ForeignKey("api_versions.id"), nullable=False)
    method_id = Column("method", Integer, ForeignKey("http_methods.id"), nullable=False)
    module_feature_id = Column(Integer, ForeignKey("modules_features.id"), nullable=False)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
    
    # Relationships
    api_version = relationship("ApiVersions", foreign_keys=[version_id])
    http_method = relationship("HttpMethods", foreign_keys=[method_id])
    module_feature = relationship("ModulesFeatures", foreign_keys=[module_feature_id])