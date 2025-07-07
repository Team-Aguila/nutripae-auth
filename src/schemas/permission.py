from pydantic import BaseModel
from typing import Optional
from .parametric import ApiVersion, HttpMethod, ModuleFeature


class PermissionBase(BaseModel):
    name: str
    version_id: int
    method_id: int
    module_feature_id: int

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    version_id: Optional[int] = None
    method_id: Optional[int] = None
    module_feature_id: Optional[int] = None

class Permission(PermissionBase):
    id: int
    module_feature: Optional[ModuleFeature] = None

    class Config:
        from_attributes = True
