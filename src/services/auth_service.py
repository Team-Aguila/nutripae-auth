from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core import security
from core.config import settings
from models.user import User
from repositories.user_repository import UserRepository
from repositories.audit_log_repository import AuditLogRepository
from schemas.token import Token
from schemas.user import UserCreate
from .user_service import UserService
from models.parametric import UserStatus

import logging

class AuthService:
    def __init__(self, user_repo: UserRepository, audit_repo: AuditLogRepository, parametric_service=None):
        self.user_repo = user_repo
        self.audit_repo = audit_repo
        self.parametric_service = parametric_service

    def register_user(self, db: Session, user_in: UserCreate) -> User:
        """
        Basic user registration
        """
        # Check if email is already registered
        db_user = self.user_repo.get_by_email(db, email=user_in.email)
        if db_user:
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
            active_status = db.query(UserStatus).filter(UserStatus.name == "ACTIVE").first()
            if not active_status:
                logging.error("Active status not found")
                raise HTTPException(status_code=500, detail="Active status not found")
        
        new_user = self.user_repo.create(db=db, obj_in=user_in, status_id=active_status.id)
        
        # Log successful registration
        self.audit_repo.create_log(
            db,
            user_id=new_user.id,
            action="user.register",
            details={"email": new_user.email}
        )
        
        return new_user

    def register_user_by_invitation(self, db: Session, user_in: UserCreate, invitation_id: int) -> User:
        """
        RF 2.5: User registration by invitation
        """
        # Check if email is already registered
        db_user = self.user_repo.get_by_email(db, email=user_in.email)
        if db_user:
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
            active_status = db.query(UserStatus).filter(UserStatus.name == "ACTIVE").first()
            if not active_status:
                logging.error("Active status not found")
                raise HTTPException(status_code=500, detail="Active status not found")
        
        new_user = self.user_repo.create(db=db, obj_in=user_in, status_id=active_status.id)
        
        # Log successful registration
        self.audit_repo.create_log(
            db,
            user_id=new_user.id,
            action="user.register_by_invitation",
            details={
                "email": new_user.email,
                "invitation_id": invitation_id
            }
        )
        
        return new_user

    def authenticate_user(self, db: Session, email: str, password: str) -> User | None:
        """
        RF 2.1.1: User authentication
        """
        user = self.user_repo.get_by_email(db, email=email)
        if not user:
            logging.error(f"User not found: {email}")
            return None
        
        # Check if user is active using parametric service
        if self.parametric_service:
            active_status = self.parametric_service.get_active_user_status(db)
            if user.status_id != active_status.id:
                logging.error(f"User is not active: {email}")
                return None
        else:
            # Fallback to direct relationship access
            if user.status.name != "ACTIVE":
                logging.error(f"User is not active: {email}")
                return None
        
        # Check if user is logically deleted
        if user.deleted_at:
            logging.error(f"User is deleted: {email}")
            return None
        
        if not security.verify_password(password, user.hashed_password):
            logging.error(f"Invalid password: {email}")
            return None
        
        # Update last login
        self.user_repo.update_last_login(db, user=user)
        
        # Log successful login
        self.audit_repo.create_log(
            db, 
            user_id=user.id, 
            action="user.login",
            details={"email": user.email}
        )
        
        return user

    def create_access_token(self, user: User) -> Token:
        """
        Create JWT access token for user
        """
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Collect all permissions from all roles
        user_permissions = []
        for role in user.roles:
            for permission in role.permissions:
                if permission.name not in user_permissions:
                    user_permissions.append(permission.name)
        
        # Get primary role (first role or None)
        primary_role = user.roles[0].name if user.roles else None
        
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "role": primary_role,
            "project_id": user.project_id,
            "permissions": user_permissions,
        }
        
        access_token = security.create_access_token(
            data=token_data, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    def change_password(self, db: Session, user: User, old_password: str, new_password: str) -> None:
        """
        RF 2.3: Change user password
        """
        if not security.verify_password(old_password, user.hashed_password):
            logging.error(f"Incorrect old password: {user.email}")
            raise HTTPException(status_code=400, detail="Incorrect old password")
        
        self.user_repo.update_password(db, user=user, new_password=new_password)
        
        # Log password change
        self.audit_repo.create_log(
            db,
            user_id=user.id,
            action="user.password_change",
            details={"email": user.email}
        )

    def get_user_permissions(self, user: User) -> List[str]:
        """Get all permissions for a user from all their roles"""
        permissions = set()
        for role in user.roles:
            for permission in role.permissions:
                permissions.add(permission.name)
        return list(permissions)
