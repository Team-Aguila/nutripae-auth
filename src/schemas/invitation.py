from pydantic import BaseModel, EmailStr, Field, validator, model_validator
from typing import List, Optional, Any
from datetime import datetime, timedelta
from .parametric import InvitationStatus

class InvitationBase(BaseModel):
    email: EmailStr

class InvitationCreate(InvitationBase):
    role_ids: List[int]
    expires_at: Optional[datetime] = None
    expires_days: Optional[int] = Field(None, description="Number of days until expiration (alternative to expires_at)")
    notes: Optional[str] = None

    @validator('expires_at', pre=True, always=True)
    def set_expires_at(cls, v, values):
        if v is not None:
            return v
        expires_days = values.get('expires_days', 7)  # Default to 7 days
        return datetime.utcnow() + timedelta(days=expires_days)

class InvitationUpdate(BaseModel):
    status_id: Optional[int] = None

class Invitation(InvitationBase):
    id: int
    code: str
    invitation_code: Optional[str] = None
    status_id: int
    created_at: datetime
    expires_at: datetime
    created_by_id: int
    roles: List['Role'] = []
    status: Optional[InvitationStatus] = None

    @model_validator(mode='before')
    @classmethod
    def set_invitation_code(cls, values: Any) -> Any:
        if isinstance(values, dict) and 'code' in values and values['code']:
            values['invitation_code'] = values['code']
        return values

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

class InvitationListItem(BaseModel):
    id: int
    code: str
    invitation_code: Optional[str] = None
    email: EmailStr
    status_id: int
    created_at: datetime
    expires_at: datetime
    roles: List['Role'] = []
    status: Optional[InvitationStatus] = None

    @model_validator(mode='before')
    @classmethod
    def set_invitation_code(cls, values: Any) -> Any:
        if isinstance(values, dict) and 'code' in values and values['code']:
            values['invitation_code'] = values['code']
        return values

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

# Import after to avoid circular imports
from .role import Role
Invitation.model_rebuild()
InvitationListItem.model_rebuild() 