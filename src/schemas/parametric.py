from pydantic import BaseModel
from typing import Optional


# User Status Schemas
class UserStatusBase(BaseModel):
    name: str

class UserStatusCreate(UserStatusBase):
    pass

class UserStatusUpdate(BaseModel):
    name: Optional[str] = None

class UserStatus(UserStatusBase):
    id: int

    class Config:
        from_attributes = True


# Invitation Status Schemas
class InvitationStatusBase(BaseModel):
    name: str

class InvitationStatusCreate(InvitationStatusBase):
    pass

class InvitationStatusUpdate(BaseModel):
    name: Optional[str] = None

class InvitationStatus(InvitationStatusBase):
    id: int

    class Config:
        from_attributes = True


# API Versions Schemas
class ApiVersionBase(BaseModel):
    name: str

class ApiVersionCreate(ApiVersionBase):
    pass

class ApiVersionUpdate(BaseModel):
    name: Optional[str] = None

class ApiVersion(ApiVersionBase):
    id: int

    class Config:
        from_attributes = True


# HTTP Methods Schemas
class HttpMethodBase(BaseModel):
    name: str

class HttpMethodCreate(HttpMethodBase):
    pass

class HttpMethodUpdate(BaseModel):
    name: Optional[str] = None

class HttpMethod(HttpMethodBase):
    id: int

    class Config:
        from_attributes = True


# Modules Schemas
class ModuleBase(BaseModel):
    name: str

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(BaseModel):
    name: Optional[str] = None

class Module(ModuleBase):
    id: int

    class Config:
        from_attributes = True


# Features Schemas
class FeatureBase(BaseModel):
    name: str

class FeatureCreate(FeatureBase):
    pass

class FeatureUpdate(BaseModel):
    name: Optional[str] = None

class Feature(FeatureBase):
    id: int

    class Config:
        from_attributes = True


# Module-Feature Relationship Schemas
class ModuleFeatureBase(BaseModel):
    module_id: int
    feature_id: int

class ModuleFeatureCreate(ModuleFeatureBase):
    pass

class ModuleFeatureUpdate(BaseModel):
    module_id: Optional[int] = None
    feature_id: Optional[int] = None

class ModuleFeature(ModuleFeatureBase):
    id: int
    module: Optional[Module] = None
    feature: Optional[Feature] = None

    class Config:
        from_attributes = True 