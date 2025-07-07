from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from models.audit_log import AuditLog
from schemas.audit_log import AuditLogCreate
import logging

class AuditLogRepository:
    def create(self, db: Session, *, obj_in: AuditLogCreate) -> AuditLog:
        db_obj = AuditLog(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logging.info(f"Audit log created: {db_obj.id}")
        return db_obj
    
    def create_log(self, db: Session, *, user_id: int, action: str, details: Optional[Dict[str, Any]] = None) -> AuditLog:
        """Helper method to create audit logs more easily"""
        log_data = AuditLogCreate(
            user_id=user_id,
            action=action,
            details=details
        )
        return self.create(db, obj_in=log_data)

    def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        logging.info(f"Getting audit logs for user: {user_id}")
        return db.query(AuditLog).filter(AuditLog.user_id == user_id).offset(skip).limit(limit).all()

    def get_by_action(self, db: Session, *, action: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        logging.info(f"Getting audit logs for action: {action}")
        return db.query(AuditLog).filter(AuditLog.action == action).offset(skip).limit(limit).all()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        logging.info("Getting all audit logs")
        return db.query(AuditLog).offset(skip).limit(limit).all()

audit_log_repository = AuditLogRepository()
