from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
import logging
from db.session import get_db
from schemas.parametric import (
    UserStatus,
    ApiVersion,
    HttpMethod,
    Module,
    Feature,
    ModuleFeature,
    InvitationStatus,
)
from services.parametric_service import ParametricService
from core.service_dependencies import get_parametric_service
from core.dependencies import require_permissions, get_current_active_user
from models.user import User as UserModel

router = APIRouter()

# User Status Endpoints
@router.get("/user-statuses/", response_model=List[UserStatus])
def list_user_statuses(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get all user statuses
    """
    logging.info(f"Listing user statuses")
    return parametric_service.get_user_statuses(db, skip=skip, limit=limit)

@router.get("/user-statuses/{status_id}", response_model=UserStatus)
def get_user_status(
    *,
    db: Session = Depends(get_db),
    status_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get user status by ID
    """
    logging.info(f"Getting user status by id: {status_id}")
    return parametric_service.get_user_status_by_id(db, status_id)

# Invitation Status Endpoints
@router.get("/invitation-statuses/", response_model=List[InvitationStatus])
def list_invitation_statuses(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get all invitation statuses
    """
    logging.info(f"Listing invitation statuses")
    return parametric_service.get_invitation_statuses(db, skip=skip, limit=limit)

@router.get("/invitation-statuses/{status_id}", response_model=InvitationStatus)
def get_invitation_status(
    *,
    db: Session = Depends(get_db),
    status_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get invitation status by ID
    """
    logging.info(f"Getting invitation status by id: {status_id}")
    return parametric_service.get_invitation_status_by_id(db, status_id)

# API Versions Endpoints
@router.get("/api-versions/", response_model=List[ApiVersion])
def list_api_versions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get all API versions
    """
    logging.info(f"Listing API versions")
    return parametric_service.get_api_versions(db, skip=skip, limit=limit)

@router.get("/api-versions/{version_id}", response_model=ApiVersion)
def get_api_version(
    *,
    db: Session = Depends(get_db),
    version_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get API version by ID
    """
    logging.info(f"Getting API version by id: {version_id}")
    return parametric_service.get_api_version_by_id(db, version_id)

# HTTP Methods Endpoints
@router.get("/http-methods/", response_model=List[HttpMethod])
def list_http_methods(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get all HTTP methods
    """
    logging.info(f"Listing HTTP methods")
    return parametric_service.get_http_methods(db, skip=skip, limit=limit)

@router.get("/http-methods/{method_id}", response_model=HttpMethod)
def get_http_method(
    *,
    db: Session = Depends(get_db),
    method_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get HTTP method by ID
    """
    logging.info(f"Getting HTTP method by id: {method_id}")
    return parametric_service.get_http_method_by_id(db, method_id)

# Modules Endpoints
@router.get("/modules/", response_model=List[Module])
def list_modules(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get all modules
    """
    logging.info(f"Listing modules")
    return parametric_service.get_modules(db, skip=skip, limit=limit)

@router.get("/modules/{module_id}", response_model=Module)
def get_module(
    *,
    db: Session = Depends(get_db),
    module_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get module by ID
    """
    logging.info(f"Getting module by id: {module_id}")
    return parametric_service.get_module_by_id(db, module_id)

# Features Endpoints
@router.get("/features/", response_model=List[Feature])
def list_features(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get all features
    """
    logging.info(f"Listing features")
    return parametric_service.get_features(db, skip=skip, limit=limit)

@router.get("/features/{feature_id}", response_model=Feature)
def get_feature(
    *,
    db: Session = Depends(get_db),
    feature_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get feature by ID
    """
    logging.info(f"Getting feature by id: {feature_id}")
    return parametric_service.get_feature_by_id(db, feature_id)

# Module-Features Endpoints
@router.get("/module-features/", response_model=List[ModuleFeature])
def list_module_features(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get all module-feature relationships
    """
    logging.info(f"Listing module features")
    return parametric_service.get_module_features(db, skip=skip, limit=limit)

@router.get("/module-features/{module_feature_id}", response_model=ModuleFeature)
def get_module_feature(
    *,
    db: Session = Depends(get_db),
    module_feature_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get module-feature relationship by ID
    """
    logging.info(f"Getting module feature by id: {module_feature_id}")
    return parametric_service.get_module_feature_by_id(db, module_feature_id)

@router.get("/modules/{module_id}/features", response_model=List[ModuleFeature])
def get_features_by_module(
    *,
    db: Session = Depends(get_db),
    module_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get features for a specific module
    """
    logging.info(f"Getting features by module: {module_id}")
    return parametric_service.get_module_features_by_module(db, module_id)

@router.get("/features/{feature_id}/modules", response_model=List[ModuleFeature])
def get_modules_by_feature(
    *,
    db: Session = Depends(get_db),
    feature_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    parametric_service: ParametricService = Depends(get_parametric_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get modules for a specific feature
    """
    logging.info(f"Getting modules by feature: {feature_id}")
    return parametric_service.get_module_features_by_feature(db, feature_id) 