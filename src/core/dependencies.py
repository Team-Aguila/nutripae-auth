from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import ValidationError
from typing import List
from sqlalchemy.orm import Session

from core.config import settings
from schemas.token import TokenData
from db.session import get_db
from repositories.user_repository import user_repository

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> TokenData:
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(
            email=payload.get("sub"),
            user_id=payload.get("user_id"),
            role=payload.get("role"),
            project_id=payload.get("project_id"),
            permissions=payload.get("permissions", [])
        )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

def require_permissions(required_permissions: List[str]):
    def permission_checker(current_user: TokenData = Depends(get_current_user)):
        user_permissions = set(current_user.permissions)
        if not all(perm in user_permissions for perm in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough permissions",
            )
        return current_user
    return permission_checker

def get_current_active_user(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    """Get the current active user from the database"""
    if not current_user.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user = user_repository.get_by_email(db, email=current_user.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if user.status.name != "ACTIVE" or user.deleted_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    
    return user

def check_authorization(user_permissions: List[str], required_permissions: List[str]) -> bool:
    """Helper function to check if user has required permissions"""
    user_perms_set = set(user_permissions)
    return all(perm in user_perms_set for perm in required_permissions)
