from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging
from models.user import User
from repositories.user_repository import UserRepository
from repositories.audit_log_repository import AuditLogRepository
from schemas.user import UserCreate, UserUpdate, UserListItem


class UserService:
    def __init__(self, user_repo: UserRepository, audit_repo: AuditLogRepository, parametric_service=None):
        self.user_repo = user_repo
        self.audit_repo = audit_repo
        self.parametric_service = parametric_service

    def create_user(self, db: Session, user_in: UserCreate, current_user_id: int) -> User:
        """
        RF 1.1.1: Crear nuevo usuario
        """
        # Check if email is already registered
        existing_user = self.user_repo.get_by_email(db, email=user_in.email)
        if existing_user:
            logging.error(f"Email already registered: {user_in.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username is already taken (if provided)
        if user_in.username:
            existing_user = self.user_repo.get_by_username(db, username=user_in.username)
            if existing_user:
                logging.error(f"Username already taken: {user_in.username}")
                raise HTTPException(status_code=400, detail="Username already taken")
        
        # Get ACTIVE status using parametric service
        if self.parametric_service:
            active_status = self.parametric_service.get_active_user_status(db)
        else:
            # Fallback to direct query for backward compatibility
            from src.models.parametric import UserStatus
            active_status = db.query(UserStatus).filter(UserStatus.name == "ACTIVE").first()
            if not active_status:
                logging.error("Active status not found")
                raise HTTPException(status_code=500, detail="Active status not found")
        
        # Create user
        new_user = self.user_repo.create(db=db, obj_in=user_in, status_id=active_status.id)
        
        # Log user creation
        self.audit_repo.create_log(
            db,
            user_id=current_user_id,
            action="usuario.crear",
            details={
                "created_user_email": new_user.email,
                "created_user_id": new_user.id,
                "roles_assigned": [role.id for role in new_user.roles]
            }
        )
        
        return new_user

    def get_users(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        status_filter: Optional[int] = None,
        role_filter: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[User]:
        """
        RF 1.1.5: Listado de usuarios
        """
        return self.user_repo.get_all(
            db, 
            skip=skip, 
            limit=limit,
            status_filter=status_filter,
            role_filter=role_filter,
            search=search
        )

    def get_user_by_id(self, db: Session, user_id: int) -> User:
        """
        RF 1.1.2: Consultar detalles de usuario
        """
        user = self.user_repo.get_by_id(db, id=user_id)
        if not user:
            logging.error(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self, db: Session, user_id: int, user_in: UserUpdate, current_user_id: int) -> User:
        """
        RF 1.1.3: Modificar datos de usuario
        """
        user = self.user_repo.get_by_id(db, id=user_id)
        if not user:
            logging.error(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        # Store old values for audit
        old_values = {
            "full_name": user.full_name,
            "email": user.email,
            "username": user.username,
            "phone_number": user.phone_number,
            "status_id": user.status_id,
            "roles": [role.id for role in user.roles]
        }
        
        # Validate unique constraints
        update_data = user_in.dict(exclude_unset=True)
        
        if "email" in update_data and update_data["email"] != user.email:
            existing_user = self.user_repo.get_by_email(db, email=update_data["email"])
            if existing_user and existing_user.id != user_id:
                logging.error(f"Email already registered: {update_data['email']}")
                raise HTTPException(status_code=400, detail="Email already registered")
        
        if "username" in update_data and update_data["username"] != user.username:
            existing_user = self.user_repo.get_by_username(db, username=update_data["username"])
            if existing_user and existing_user.id != user_id:
                logging.error(f"Username already taken: {update_data['username']}")
                raise HTTPException(status_code=400, detail="Username already taken")
        
        # Update user
        updated_user = self.user_repo.update(db, db_obj=user, obj_in=user_in)
        
        # Log user update with changed fields
        new_values = {
            "full_name": updated_user.full_name,
            "email": updated_user.email,
            "username": updated_user.username,
            "phone_number": updated_user.phone_number,
            "status_id": updated_user.status_id,
            "roles": [role.id for role in updated_user.roles]
        }
        
        changed_fields = {}
        for field, old_value in old_values.items():
            new_value = new_values[field]
            if old_value != new_value:
                changed_fields[field] = {"old": old_value, "new": new_value}
        
        if changed_fields:  # Only log if there were actual changes
            self.audit_repo.create_log(
                db,
                user_id=current_user_id,
                action="usuario.editar",
                details={
                    "modified_user_id": user_id,
                    "modified_user_email": updated_user.email,
                    "changed_fields": changed_fields
                }
            )
        
        return updated_user

    def delete_user_logical(self, db: Session, user_id: int, current_user_id: int) -> User:
        """
        RF 1.1.4: Eliminación lógica de usuario
        """
        if user_id == current_user_id:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")
        
        user = self.user_repo.get_by_id(db, id=user_id)
        if not user:
            logging.error(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.deleted_at:
            raise HTTPException(status_code=400, detail="User already deleted")
        
        # Delete user logically
        deleted_user = self.user_repo.delete_logical(db, id=user_id)
        
        # Log user deletion
        self.audit_repo.create_log(
            db,
            user_id=current_user_id,
            action="usuario.eliminar",
            details={
                "deleted_user_id": user_id,
                "deleted_user_email": user.email
            }
        )
        
        return deleted_user 