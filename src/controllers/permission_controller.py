from typing import List
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import Optional
import logging
from db.session import get_db
from schemas.permission import Permission
from services.permission_service import PermissionService
from core.service_dependencies import get_permission_service
from core.dependencies import require_permissions, get_current_active_user
from models.user import User as UserModel

router = APIRouter()

@router.get("/", response_model=List[Permission])
def list_permissions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    permission_service: PermissionService = Depends(get_permission_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    RF 1.3.1: Consultar catálogo de permisos
    Muestra un listado de todos los permisos definidos en el sistema
    """
    logging.info(f"Listing permissions")
    return permission_service.get_permissions(db, skip=skip, limit=limit)

@router.get("/{permission_id}", response_model=Permission)
def get_permission(
    *,
    db: Session = Depends(get_db),
    permission_id: int = Path(..., description="Permission ID"),
    current_user: UserModel = Depends(get_current_active_user),
    permission_service: PermissionService = Depends(get_permission_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get permission by ID
    """
    logging.info(f"Getting permission by id: {permission_id}")
    return permission_service.get_permission_by_id(db, permission_id)

@router.get("/by-name/{permission_name}", response_model=Permission)
def get_permission_by_name(
    *,
    db: Session = Depends(get_db),
    permission_name: str = Path(..., description="Permission name"),
    current_user: UserModel = Depends(get_current_active_user),
    permission_service: PermissionService = Depends(get_permission_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get permission by name
    """
    logging.info(f"Getting permission by name: {permission_name}")
    return permission_service.get_permission_by_name(db, permission_name)

@router.get("/by-version/{version_name}", response_model=List[Permission])
def get_permissions_by_version(
    *,
    db: Session = Depends(get_db),
    version_name: str = Path(..., description="API version name (e.g. 'v1', 'v2')"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    permission_service: PermissionService = Depends(get_permission_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get permissions filtered by API version
    """
    logging.info(f"Getting permissions by version: {version_name}")
    return permission_service.get_permissions_by_version(db, version_name, skip=skip, limit=limit)

@router.get("/by-method/{method_name}", response_model=List[Permission])
def get_permissions_by_method(
    *,
    db: Session = Depends(get_db),
    method_name: str = Path(..., description="HTTP method name (e.g. 'GET', 'POST')"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    permission_service: PermissionService = Depends(get_permission_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get permissions filtered by HTTP method
    """
    logging.info(f"Getting permissions by method: {method_name}")
    return permission_service.get_permissions_by_method(db, method_name, skip=skip, limit=limit)

@router.get("/by-module-feature/{module_name}/{feature_name}", response_model=List[Permission])
def get_permissions_by_module_feature(
    *,
    db: Session = Depends(get_db),
    module_name: str = Path(..., description="Module name"),
    feature_name: str = Path(..., description="Feature name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    permission_service: PermissionService = Depends(get_permission_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Get permissions filtered by module and feature
    """
    logging.info(f"Getting permissions by module and feature: {module_name} {feature_name}")
    return permission_service.get_permissions_by_module_feature(
        db, module_name, feature_name, skip=skip, limit=limit
    )

@router.get("/search", response_model=List[Permission])
def search_permissions(
    db: Session = Depends(get_db),
    version_name: Optional[str] = Query(None, description="Filter by API version"),
    method_name: Optional[str] = Query(None, description="Filter by HTTP method"),
    module_name: Optional[str] = Query(None, description="Filter by module name"),
    feature_name: Optional[str] = Query(None, description="Filter by feature name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    permission_service: PermissionService = Depends(get_permission_service),
    _: dict = Depends(require_permissions(["permission:list"]))
):
    """
    Advanced search for permissions with multiple filters
    """
    logging.info(f"Searching permissions with filters: version_name={version_name}, method_name={method_name}, module_name={module_name}, feature_name={feature_name}")
    return permission_service.get_permissions_filtered(
        db, 
        version_name=version_name,
        method_name=method_name,
        module_name=module_name,
        feature_name=feature_name,
        skip=skip, 
        limit=limit
    ) 