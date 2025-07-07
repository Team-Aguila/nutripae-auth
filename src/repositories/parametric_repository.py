from sqlalchemy.orm import Session
from typing import List
from models.parametric import (
    UserStatus,
    InvitationStatus, 
    ApiVersions,
    HttpMethods,
    Modules,
    Features,
    ModulesFeatures
)
import logging

class ParametricRepository:
    
    # User Status methods
    def get_user_status_by_id(self, db: Session, *, id: int) -> UserStatus | None:
        logging.info(f"Getting user status by id: {id}")
        return db.query(UserStatus).filter(UserStatus.id == id).first()
    
    def get_user_status_by_name(self, db: Session, *, name: str) -> UserStatus | None:
        logging.info(f"Getting user status by name: {name}")
        return db.query(UserStatus).filter(UserStatus.name == name).first()
    
    def get_all_user_statuses(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserStatus]:
        logging.info("Getting all user statuses")
        return db.query(UserStatus).offset(skip).limit(limit).all()
    
    # Invitation Status methods
    def get_invitation_status_by_id(self, db: Session, *, id: int) -> InvitationStatus | None:
        logging.info(f"Getting invitation status by id: {id}")
        return db.query(InvitationStatus).filter(InvitationStatus.id == id).first()
    
    def get_invitation_status_by_name(self, db: Session, *, name: str) -> InvitationStatus | None:
        logging.info(f"Getting invitation status by name: {name}")
        return db.query(InvitationStatus).filter(InvitationStatus.name == name).first()
    
    def get_all_invitation_statuses(self, db: Session, skip: int = 0, limit: int = 100) -> List[InvitationStatus]:
        logging.info("Getting all invitation statuses")
        return db.query(InvitationStatus).offset(skip).limit(limit).all()
    
    # API Versions methods
    def get_api_version_by_id(self, db: Session, *, id: int) -> ApiVersions | None:
        logging.info(f"Getting API version by id: {id}")
        return db.query(ApiVersions).filter(ApiVersions.id == id).first()
    
    def get_api_version_by_name(self, db: Session, *, name: str) -> ApiVersions | None:
        logging.info(f"Getting API version by name: {name}")
        return db.query(ApiVersions).filter(ApiVersions.name == name).first()
    
    def get_all_api_versions(self, db: Session, skip: int = 0, limit: int = 100) -> List[ApiVersions]:
        logging.info("Getting all API versions")
        return db.query(ApiVersions).offset(skip).limit(limit).all()
    
    # HTTP Methods methods
    def get_http_method_by_id(self, db: Session, *, id: int) -> HttpMethods | None:
        logging.info(f"Getting HTTP method by id: {id}")
        return db.query(HttpMethods).filter(HttpMethods.id == id).first()
    
    def get_http_method_by_name(self, db: Session, *, name: str) -> HttpMethods | None:
        logging.info(f"Getting HTTP method by name: {name}")
        return db.query(HttpMethods).filter(HttpMethods.name == name).first()
    
    def get_all_http_methods(self, db: Session, skip: int = 0, limit: int = 100) -> List[HttpMethods]:
        logging.info("Getting all HTTP methods")
        return db.query(HttpMethods).offset(skip).limit(limit).all()
    
    # Modules methods
    def get_module_by_id(self, db: Session, *, id: int) -> Modules | None:
        logging.info(f"Getting module by id: {id}")
        return db.query(Modules).filter(Modules.id == id).first()
    
    def get_module_by_name(self, db: Session, *, name: str) -> Modules | None:
        logging.info(f"Getting module by name: {name}")
        return db.query(Modules).filter(Modules.name == name).first()
    
    def get_all_modules(self, db: Session, skip: int = 0, limit: int = 100) -> List[Modules]:
        logging.info("Getting all modules")
        return db.query(Modules).offset(skip).limit(limit).all()
    
    # Features methods
    def get_feature_by_id(self, db: Session, *, id: int) -> Features | None:
        logging.info(f"Getting feature by id: {id}")
        return db.query(Features).filter(Features.id == id).first()
    
    def get_feature_by_name(self, db: Session, *, name: str) -> Features | None:
        logging.info(f"Getting feature by name: {name}")
        return db.query(Features).filter(Features.name == name).first()
    
    def get_all_features(self, db: Session, skip: int = 0, limit: int = 100) -> List[Features]:
        logging.info("Getting all features")
        return db.query(Features).offset(skip).limit(limit).all()
    
    # Module-Features relationship methods
    def get_module_feature_by_id(self, db: Session, *, id: int) -> ModulesFeatures | None:
        logging.info(f"Getting module feature by id: {id}")
        return db.query(ModulesFeatures).filter(ModulesFeatures.id == id).first()
    
    def get_module_features_by_module(self, db: Session, *, module_id: int) -> List[ModulesFeatures]:
        logging.info(f"Getting module features by module: {module_id}")
        return db.query(ModulesFeatures).filter(ModulesFeatures.module_id == module_id).all()
    
    def get_module_features_by_feature(self, db: Session, *, feature_id: int) -> List[ModulesFeatures]:
        logging.info(f"Getting module features by feature: {feature_id}")
        return db.query(ModulesFeatures).filter(ModulesFeatures.feature_id == feature_id).all()
    
    def get_all_module_features(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModulesFeatures]:
        logging.info("Getting all module features")
        return db.query(ModulesFeatures).offset(skip).limit(limit).all()


parametric_repository = ParametricRepository() 