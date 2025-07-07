from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging
from models.parametric import (
    UserStatus,
    InvitationStatus,
    ApiVersions,
    HttpMethods,
    Modules,
    Features,
    ModulesFeatures
)
from repositories.parametric_repository import ParametricRepository
from repositories.audit_log_repository import AuditLogRepository
from schemas.parametric import (
    UserStatusCreate, UserStatusUpdate,
    InvitationStatusCreate, InvitationStatusUpdate,
    ApiVersionCreate, ApiVersionUpdate,
    HttpMethodCreate, HttpMethodUpdate,
    ModuleCreate, ModuleUpdate,
    FeatureCreate, FeatureUpdate,
    ModuleFeatureCreate, ModuleFeatureUpdate
)


class ParametricService:
    def __init__(self, parametric_repo: ParametricRepository, audit_repo: AuditLogRepository):
        self.parametric_repo = parametric_repo
        self.audit_repo = audit_repo

    # User Status Services
    def get_user_statuses(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserStatus]:
        """Get all user statuses"""
        return self.parametric_repo.get_all_user_statuses(db, skip=skip, limit=limit)

    def get_user_status_by_id(self, db: Session, status_id: int) -> UserStatus:
        """Get user status by ID"""
        status = self.parametric_repo.get_user_status_by_id(db, id=status_id)
        if not status:
            logging.error(f"User status not found: {status_id}")
            raise HTTPException(status_code=404, detail="User status not found")
        return status

    def get_user_status_by_name(self, db: Session, name: str) -> UserStatus:
        """Get user status by name"""
        status = self.parametric_repo.get_user_status_by_name(db, name=name)
        if not status:
            logging.error(f"User status not found: {name}")
            raise HTTPException(status_code=404, detail="User status not found")
        return status

    # Invitation Status Services
    def get_invitation_statuses(self, db: Session, skip: int = 0, limit: int = 100) -> List[InvitationStatus]:
        """Get all invitation statuses"""
        return self.parametric_repo.get_all_invitation_statuses(db, skip=skip, limit=limit)

    def get_invitation_status_by_id(self, db: Session, status_id: int) -> InvitationStatus:
        """Get invitation status by ID"""
        status = self.parametric_repo.get_invitation_status_by_id(db, id=status_id)
        if not status:
            logging.error(f"Invitation status not found: {status_id}")
            raise HTTPException(status_code=404, detail="Invitation status not found")
        return status

    def get_invitation_status_by_name(self, db: Session, name: str) -> InvitationStatus:
        """Get invitation status by name"""
        status = self.parametric_repo.get_invitation_status_by_name(db, name=name)
        if not status:
            logging.error(f"Invitation status not found: {name}")
            raise HTTPException(status_code=404, detail="Invitation status not found")
        return status

    # API Versions Services
    def get_api_versions(self, db: Session, skip: int = 0, limit: int = 100) -> List[ApiVersions]:
        """Get all API versions"""
        return self.parametric_repo.get_all_api_versions(db, skip=skip, limit=limit)

    def get_api_version_by_id(self, db: Session, version_id: int) -> ApiVersions:
        """Get API version by ID"""
        version = self.parametric_repo.get_api_version_by_id(db, id=version_id)
        if not version:
            logging.error(f"API version not found: {version_id}")
            raise HTTPException(status_code=404, detail="API version not found")
        return version

    def get_api_version_by_name(self, db: Session, name: str) -> ApiVersions:
        """Get API version by name"""
        version = self.parametric_repo.get_api_version_by_name(db, name=name)
        if not version:
            logging.error(f"API version not found: {name}")
            raise HTTPException(status_code=404, detail="API version not found")
        return version

    # HTTP Methods Services
    def get_http_methods(self, db: Session, skip: int = 0, limit: int = 100) -> List[HttpMethods]:
        """Get all HTTP methods"""
        return self.parametric_repo.get_all_http_methods(db, skip=skip, limit=limit)

    def get_http_method_by_id(self, db: Session, method_id: int) -> HttpMethods:
        """Get HTTP method by ID"""
        method = self.parametric_repo.get_http_method_by_id(db, id=method_id)
        if not method:
            logging.error(f"HTTP method not found: {method_id}")
            raise HTTPException(status_code=404, detail="HTTP method not found")
        return method

    def get_http_method_by_name(self, db: Session, name: str) -> HttpMethods:
        """Get HTTP method by name"""
        method = self.parametric_repo.get_http_method_by_name(db, name=name)
        if not method:
            logging.error(f"HTTP method not found: {name}")
            raise HTTPException(status_code=404, detail="HTTP method not found")
        return method

    # Modules Services
    def get_modules(self, db: Session, skip: int = 0, limit: int = 100) -> List[Modules]:
        """Get all modules"""
        return self.parametric_repo.get_all_modules(db, skip=skip, limit=limit)

    def get_module_by_id(self, db: Session, module_id: int) -> Modules:
        """Get module by ID"""
        module = self.parametric_repo.get_module_by_id(db, id=module_id)
        if not module:
            logging.error(f"Module not found: {module_id}")
            raise HTTPException(status_code=404, detail="Module not found")
        return module

    def get_module_by_name(self, db: Session, name: str) -> Modules:
        """Get module by name"""
        module = self.parametric_repo.get_module_by_name(db, name=name)
        if not module:
            logging.error(f"Module not found: {name}")
            raise HTTPException(status_code=404, detail="Module not found")
        return module

    # Features Services
    def get_features(self, db: Session, skip: int = 0, limit: int = 100) -> List[Features]:
        """Get all features"""
        return self.parametric_repo.get_all_features(db, skip=skip, limit=limit)

    def get_feature_by_id(self, db: Session, feature_id: int) -> Features:
        """Get feature by ID"""
        feature = self.parametric_repo.get_feature_by_id(db, id=feature_id)
        if not feature:
            raise HTTPException(status_code=404, detail="Feature not found")
        return feature

    def get_feature_by_name(self, db: Session, name: str) -> Features:
        """Get feature by name"""
        feature = self.parametric_repo.get_feature_by_name(db, name=name)
        if not feature:
            raise HTTPException(status_code=404, detail="Feature not found")
        return feature

    # Module-Features Services
    def get_module_features(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModulesFeatures]:
        """Get all module-feature relationships"""
        return self.parametric_repo.get_all_module_features(db, skip=skip, limit=limit)

    def get_module_feature_by_id(self, db: Session, module_feature_id: int) -> ModulesFeatures:
        """Get module-feature relationship by ID"""
        module_feature = self.parametric_repo.get_module_feature_by_id(db, id=module_feature_id)
        if not module_feature:
            raise HTTPException(status_code=404, detail="Module-feature relationship not found")
        return module_feature

    def get_module_features_by_module(self, db: Session, module_id: int) -> List[ModulesFeatures]:
        """Get features for a specific module"""
        return self.parametric_repo.get_module_features_by_module(db, module_id=module_id)

    def get_module_features_by_feature(self, db: Session, feature_id: int) -> List[ModulesFeatures]:
        """Get modules for a specific feature"""
        return self.parametric_repo.get_module_features_by_feature(db, feature_id=feature_id)

    # Utility methods for other services
    def get_active_user_status(self, db: Session) -> UserStatus:
        """Get ACTIVE user status - utility for other services"""
        return self.get_user_status_by_name(db, "ACTIVE")

    def get_pending_invitation_status(self, db: Session) -> InvitationStatus:
        """Get PENDING invitation status - utility for other services"""
        return self.get_invitation_status_by_name(db, "PENDING")

    def get_cancelled_invitation_status(self, db: Session) -> InvitationStatus:
        """Get CANCELLED invitation status - utility for other services"""
        return self.get_invitation_status_by_name(db, "CANCELLED")

    def get_accepted_invitation_status(self, db: Session) -> InvitationStatus:
        """Get ACCEPTED invitation status - utility for other services"""
        return self.get_invitation_status_by_name(db, "ACCEPTED")

    def get_expired_invitation_status(self, db: Session) -> InvitationStatus:
        """Get EXPIRED invitation status - utility for other services"""
        return self.get_invitation_status_by_name(db, "EXPIRED")

    def get_deleted_user_status(self, db: Session) -> UserStatus:
        """Get DELETED user status - utility for other services"""
        return self.get_user_status_by_name(db, "DELETED") 