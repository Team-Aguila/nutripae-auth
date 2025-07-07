from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime
from .role import Role
from .project import Project
from .parametric import UserStatus

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    username: Optional[str] = None
    phone_number: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    password: str
    project_id: Optional[int] = None
    role_ids: List[int] = []
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    status_id: Optional[int] = None
    role_ids: Optional[List[int]] = None

class User(UserBase):
    id: int
    status_id: int
    project_id: Optional[int] = None
    created_at: datetime
    last_login_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    roles: List[Role] = []
    project: Optional[Project] = None
    status: Optional[UserStatus] = None

    class Config:
        from_attributes = True

class UserListItem(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    username: Optional[str] = None
    status_id: int
    created_at: datetime
    last_login_at: Optional[datetime] = None
    roles: List[Role] = []
    status: Optional[UserStatus] = None

    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v
