from services.auth_service import AuthService
from services.user_service import UserService
from services.role_service import RoleService
from services.permission_service import PermissionService
from services.invitation_service import InvitationService
from services.parametric_service import ParametricService

from repositories.user_repository import user_repository
from repositories.role_repository import role_repository
from repositories.permission_repository import permission_repository
from repositories.invitation_repository import invitation_repository
from repositories.audit_log_repository import audit_log_repository
from repositories.parametric_repository import parametric_repository


def get_parametric_service() -> ParametricService:
    """Get ParametricService with injected dependencies"""
    return ParametricService(
        parametric_repo=parametric_repository,
        audit_repo=audit_log_repository
    )


def get_auth_service() -> AuthService:
    """Get AuthService with injected dependencies"""
    return AuthService(
        user_repo=user_repository,
        audit_repo=audit_log_repository,
        parametric_service=get_parametric_service()
    )


def get_user_service() -> UserService:
    """Get UserService with injected dependencies"""
    return UserService(
        user_repo=user_repository,
        audit_repo=audit_log_repository,
        parametric_service=get_parametric_service()
    )


def get_role_service() -> RoleService:
    """Get RoleService with injected dependencies"""
    return RoleService(
        role_repo=role_repository,
        audit_repo=audit_log_repository
    )


def get_permission_service() -> PermissionService:
    """Get PermissionService with injected dependencies"""
    return PermissionService(
        permission_repo=permission_repository,
        parametric_service=get_parametric_service()
    )


def get_invitation_service() -> InvitationService:
    """Get InvitationService with injected dependencies"""
    return InvitationService(
        invitation_repo=invitation_repository,
        audit_repo=audit_log_repository,
        parametric_service=get_parametric_service()
    )


def get_parametric_repository():
    """Get ParametricRepository instance"""
    return parametric_repository 