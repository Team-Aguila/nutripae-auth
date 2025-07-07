from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.permission import Permission
import logging
class PermissionRepository:
    def get_by_id(self, db: Session, *, id: int) -> Permission | None:
        logging.info(f"Getting permission by id: {id}")
        return db.query(Permission).options(
            joinedload(Permission.module_feature)
        ).filter(Permission.id == id).first()
    
    def get_by_name(self, db: Session, *, name: str) -> Permission | None:
        logging.info(f"Getting permission by name: {name}")
        return db.query(Permission).options(
            joinedload(Permission.module_feature)
        ).filter(Permission.name == name).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Permission]:
        logging.info("Getting all permissions")
        return db.query(Permission).options(
            joinedload(Permission.module_feature)
        ).offset(skip).limit(limit).all()

    def get_by_ids(self, db: Session, *, ids: List[int]) -> List[Permission]:
        logging.info(f"Getting permissions by ids: {ids}")
        return db.query(Permission).options(
            joinedload(Permission.module_feature)
        ).filter(Permission.id.in_(ids)).all()

    def get_by_version(self, db: Session, *, version_id: int, skip: int = 0, limit: int = 100) -> List[Permission]:
        """Get permissions by API version"""
        logging.info(f"Getting permissions by version: {version_id}")
        return db.query(Permission).options(
            joinedload(Permission.module_feature)
        ).filter(Permission.version_id == version_id).offset(skip).limit(limit).all()

    def get_by_method(self, db: Session, *, method_id: str, skip: int = 0, limit: int = 100) -> List[Permission]:
        """Get permissions by HTTP method"""
        logging.info(f"Getting permissions by method: {method_id}")
        return db.query(Permission).options(
            joinedload(Permission.module_feature)
        ).filter(Permission.method_id == method_id).offset(skip).limit(limit).all()

    def get_by_module_feature(self, db: Session, *, module_feature_id: int, skip: int = 0, limit: int = 100) -> List[Permission]:
        """Get permissions by module-feature relationship"""
        logging.info(f"Getting permissions by module-feature: {module_feature_id}")
        return db.query(Permission).options(
            joinedload(Permission.module_feature)
        ).filter(Permission.module_feature_id == module_feature_id).offset(skip).limit(limit).all()

    def get_by_filters(self, db: Session, *, 
                      version_id: Optional[int] = None,
                      method_id: Optional[str] = None,
                      module_feature_id: Optional[int] = None,
                      skip: int = 0, limit: int = 100) -> List[Permission]:
        """Get permissions with multiple filters"""
        logging.info(f"Getting permissions with filters: version_id={version_id}, method_id={method_id}, module_feature_id={module_feature_id}")
        query = db.query(Permission).options(
            joinedload(Permission.module_feature)
        )
        
        if version_id:
            query = query.filter(Permission.version_id == version_id)
        if method_id:
            query = query.filter(Permission.method_id == method_id)
        if module_feature_id:
            query = query.filter(Permission.module_feature_id == module_feature_id)
        
        return query.offset(skip).limit(limit).all()

permission_repository = PermissionRepository() 