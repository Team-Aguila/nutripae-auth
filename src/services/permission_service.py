from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging
from models.permission import Permission
from repositories.permission_repository import PermissionRepository


class PermissionService:
    def __init__(self, permission_repo: PermissionRepository, parametric_service=None):
        self.permission_repo = permission_repo
        self.parametric_service = parametric_service

    def get_permissions(self, db: Session, skip: int = 0, limit: int = 100) -> List[Permission]:
        """
        RF 1.3.1: Consultar catálogo de permisos
        """
        return self.permission_repo.get_all(db, skip=skip, limit=limit)

    def get_permission_by_id(self, db: Session, permission_id: int) -> Permission:
        """
        Get permission by ID
        """
        permission = self.permission_repo.get_by_id(db, id=permission_id)
        if not permission:
            logging.error(f"Permission not found: {permission_id}")
            raise HTTPException(status_code=404, detail="Permission not found")
        return permission

    def get_permission_by_name(self, db: Session, name: str) -> Permission:
        """
        Get permission by name
        """
        permission = self.permission_repo.get_by_name(db, name=name)
        if not permission:
            logging.error(f"Permission not found: {name}")
            raise HTTPException(status_code=404, detail="Permission not found")
        return permission

    def get_permissions_by_version(self, db: Session, version_name: str, skip: int = 0, limit: int = 100) -> List[Permission]:
        """
        Get permissions by API version name
        """
        if self.parametric_service:
            api_version = self.parametric_service.get_api_version_by_name(db, version_name)
            return self.permission_repo.get_by_version(db, version_id=api_version.id, skip=skip, limit=limit)
        else:
            raise HTTPException(status_code=500, detail="Parametric service not available")

    def get_permissions_by_method(self, db: Session, method_name: str, skip: int = 0, limit: int = 100) -> List[Permission]:
        """
        Get permissions by HTTP method name
        """
        if self.parametric_service:
            http_method = self.parametric_service.get_http_method_by_name(db, method_name)
            return self.permission_repo.get_by_method(db, method_id=http_method.id, skip=skip, limit=limit)
        else:
            raise HTTPException(status_code=500, detail="Parametric service not available")

    def get_permissions_by_module_feature(self, db: Session, module_name: str, feature_name: str, skip: int = 0, limit: int = 100) -> List[Permission]:
        """
        Get permissions by module and feature names
        """
        if self.parametric_service:
            # Get module and feature
            module = self.parametric_service.get_module_by_name(db, module_name)
            feature = self.parametric_service.get_feature_by_name(db, feature_name)
            
            # Get module-feature relationship
            module_features = self.parametric_service.get_module_features_by_module(db, module.id)
            module_feature = next((mf for mf in module_features if mf.feature_id == feature.id), None)
            
            if not module_feature:
                logging.error(f"Module-feature relationship not found for {module_name}-{feature_name}")
                raise HTTPException(status_code=404, detail=f"Module-feature relationship not found for {module_name}-{feature_name}")
            
            return self.permission_repo.get_by_module_feature(db, module_feature_id=module_feature.id, skip=skip, limit=limit)
        else:
            raise HTTPException(status_code=500, detail="Parametric service not available")

    def get_permissions_filtered(self, db: Session, 
                                version_name: Optional[str] = None,
                                method_name: Optional[str] = None,
                                module_name: Optional[str] = None,
                                feature_name: Optional[str] = None,
                                skip: int = 0, limit: int = 100) -> List[Permission]:
        """
        Get permissions with multiple filters using parametric names
        """
        if not self.parametric_service:
            logging.error("Parametric service not available")
            raise HTTPException(status_code=500, detail="Parametric service not available")
        
        version_id = None
        method_id = None
        module_feature_id = None
        
        # Convert version name to ID
        if version_name:
            api_version = self.parametric_service.get_api_version_by_name(db, version_name)
            if not api_version:
                logging.error(f"API version not found: {version_name}")
            version_id = api_version.id
        
        # Convert method name to ID
        if method_name:
            http_method = self.parametric_service.get_http_method_by_name(db, method_name)
            if not http_method:
                logging.error(f"HTTP method not found: {method_name}")
            method_id = http_method.id
        
        # Convert module-feature names to relationship ID
        if module_name and feature_name:
            module = self.parametric_service.get_module_by_name(db, module_name)
            if not module:
                logging.error(f"Module not found: {module_name}")
            feature = self.parametric_service.get_feature_by_name(db, feature_name)
            if not feature:
                logging.error(f"Feature not found: {feature_name}")
            module_features = self.parametric_service.get_module_features_by_module(db, module.id)
            module_feature = next((mf for mf in module_features if mf.feature_id == feature.id), None)
            
            if module_feature:
                module_feature_id = module_feature.id
        
        return self.permission_repo.get_by_filters(
            db,
            version_id=version_id,
            method_id=method_id,
            module_feature_id=module_feature_id,
            skip=skip,
            limit=limit
        ) 