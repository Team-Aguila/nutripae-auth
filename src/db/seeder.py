from sqlalchemy.orm import Session
from models.permission import Permission
from models.role import Role
from models.project import Project
from models.user import User
from models.parametric import (
    UserStatus, 
    InvitationStatus,
    ApiVersions,
    HttpMethods,
    Modules,
    Features,
    ModulesFeatures
)
from repositories.user_repository import user_repository
from schemas.user import UserCreate
from core.config import settings

# Basic parametric data
USER_STATUSES = ["ACTIVE", "INACTIVE", "DELETED"]
INVITATION_STATUSES = ["PENDING", "ACCEPTED", "EXPIRED", "CANCELLED"]
API_VERSIONS = ["v1", "v2"]
HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
MODULES = ["auth", "user", "role", "permission", "invitation", "project", "nutripae-rh", "nutripae-cobertura"]
FEATURES = ["create", "read", "update", "delete", "list", "manage"]

# Module-Feature relationships
MODULE_FEATURES = [
    ("auth", "read"),
    ("auth", "create"), 
    ("auth", "update"),
    ("user", "create"),
    ("user", "read"),
    ("user", "update"), 
    ("user", "delete"),
    ("user", "list"),
    ("role", "create"),
    ("role", "read"),
    ("role", "update"),
    ("role", "delete"),
    ("role", "list"),
    ("permission", "list"),
    ("invitation", "create"),
    ("invitation", "list"),
    ("invitation", "manage"),
    ("project", "create"),
    ("project", "read"),
    ("project", "update"),
    ("project", "delete"),
    ("nutripae-rh", "create"),
    ("nutripae-rh", "read"),
    ("nutripae-rh", "update"),
    ("nutripae-rh", "delete"),
    ("nutripae-rh", "list"),
    ("nutripae-cobertura", "create"),
    ("nutripae-cobertura", "read"),
    ("nutripae-cobertura", "update"),
    ("nutripae-cobertura", "delete"),
    ("nutripae-cobertura", "list"),
]

# Permissions with granular structure: (name, version, method, module_name, feature_name)
PERMISSIONS = [
    # User permissions
    ("user:create", "v1", "POST", "user", "create"),
    ("user:read", "v1", "GET", "user", "read"),
    ("user:list", "v1", "GET", "user", "list"),
    ("user:update", "v1", "PUT", "user", "update"),
    ("user:delete", "v1", "DELETE", "user", "delete"),
    ("user:read_own", "v1", "GET", "auth", "read"),
    ("user:update_own", "v1", "PUT", "auth", "update"),
    
    # Role permissions
    ("role:create", "v1", "POST", "role", "create"),
    ("role:read", "v1", "GET", "role", "read"),
    ("role:list", "v1", "GET", "role", "list"),
    ("role:update", "v1", "PUT", "role", "update"),
    ("role:delete", "v1", "DELETE", "role", "delete"),
    
    # Permission permissions
    ("permission:list", "v1", "GET", "permission", "list"),
    
    # Invitation permissions
    ("invitation:create", "v1", "POST", "invitation", "create"),
    ("invitation:list", "v1", "GET", "invitation", "list"),
    
    # Project permissions
    ("project:create", "v1", "POST", "project", "create"),
    ("project:read", "v1", "GET", "project", "read"),
    ("project:update", "v1", "PUT", "project", "update"),
    ("project:delete", "v1", "DELETE", "project", "delete"),

    # Human Resources permissions
    ("nutripae-rh:create", "v1", "POST", "nutripae-rh", "create"),
    ("nutripae-rh:read", "v1", "GET", "nutripae-rh", "read"),
    ("nutripae-rh:update", "v1", "PUT", "nutripae-rh", "update"),
    ("nutripae-rh:delete", "v1", "DELETE", "nutripae-rh", "delete"),
    ("nutripae-rh:list", "v1", "GET", "nutripae-rh", "list"),

    # Coverage permissions
    ("nutripae-cobertura:create", "v1", "POST", "nutripae-cobertura", "create"),
    ("nutripae-cobertura:read", "v1", "GET", "nutripae-cobertura", "read"),
    ("nutripae-cobertura:update", "v1", "PUT", "nutripae-cobertura", "update"),
    ("nutripae-cobertura:delete", "v1", "DELETE", "nutripae-cobertura", "delete"),
    ("nutripae-cobertura:list", "v1", "GET", "nutripae-cobertura", "list"),
]

ROLES = {
    "Super Admin": [perm[0] for perm in PERMISSIONS],  # All permissions by name
    "Project Admin": [
        "user:create",
        "user:read", 
        "user:list",
        "user:update",
        "user:delete",
        "role:read",
        "role:list",
        "invitation:create",
        "invitation:list",
        "project:read",
        "project:update",
        "nutripae-rh:create",
        "nutripae-rh:read",
        "nutripae-rh:update",
        "nutripae-rh:delete",
        "nutripae-rh:list",
        "nutripae-cobertura:create",
        "nutripae-cobertura:read",
        "nutripae-cobertura:update",
        "nutripae-cobertura:delete",
        "nutripae-cobertura:list",
    ],
    "Basic User": [
        "user:read_own",
        "user:update_own",
        "project:read",
    ],
    "NutriPAE-RH User": [
        "nutripae-rh:read",
        "nutripae-rh:list",
    ],
    "NutriPAE-RH Admin": [
        "nutripae-rh:create",
        "nutripae-rh:read",
        "nutripae-rh:update",
        "nutripae-rh:delete",
        "nutripae-rh:list",
    ],
    "NutriPAE-Cobertura User": [
        "nutripae-cobertura:read",
        "nutripae-cobertura:list",
    ],
    "NutriPAE-Cobertura Admin": [
        "nutripae-cobertura:create",
        "nutripae-cobertura:read",
        "nutripae-cobertura:update",
        "nutripae-cobertura:delete",
        "nutripae-cobertura:list",
    ],
}

def seed_db(db: Session):
    # Create User Statuses
    for status_name in USER_STATUSES:
        status = db.query(UserStatus).filter(UserStatus.name == status_name).first()
        if not status:
            db.add(UserStatus(name=status_name))
    db.commit()
    
    # Create Invitation Statuses
    for status_name in INVITATION_STATUSES:
        status = db.query(InvitationStatus).filter(InvitationStatus.name == status_name).first()
        if not status:
            db.add(InvitationStatus(name=status_name))
    db.commit()

    # Create API Versions
    for version_name in API_VERSIONS:
        version = db.query(ApiVersions).filter(ApiVersions.name == version_name).first()
        if not version:
            db.add(ApiVersions(name=version_name))
    db.commit()

    # Create HTTP Methods
    for method_name in HTTP_METHODS:
        method = db.query(HttpMethods).filter(HttpMethods.name == method_name).first()
        if not method:
            db.add(HttpMethods(name=method_name))
    db.commit()

    # Create Modules
    for module_name in MODULES:
        module = db.query(Modules).filter(Modules.name == module_name).first()
        if not module:
            db.add(Modules(name=module_name))
    db.commit()

    # Create Features
    for feature_name in FEATURES:
        feature = db.query(Features).filter(Features.name == feature_name).first()
        if not feature:
            db.add(Features(name=feature_name))
    db.commit()

    # Create Module-Feature relationships
    for module_name, feature_name in MODULE_FEATURES:
        module = db.query(Modules).filter(Modules.name == module_name).first()
        feature = db.query(Features).filter(Features.name == feature_name).first()
        
        if module and feature:
            existing = db.query(ModulesFeatures).filter(
                ModulesFeatures.module_id == module.id,
                ModulesFeatures.feature_id == feature.id
            ).first()
            
            if not existing:
                db.add(ModulesFeatures(module_id=module.id, feature_id=feature.id))
    db.commit()

    # Create Permissions with granular structure
    for perm_name, version_name, method_name, module_name, feature_name in PERMISSIONS:
        existing_permission = db.query(Permission).filter(Permission.name == perm_name).first()
        
        if not existing_permission:
            # Get foreign key IDs
            version = db.query(ApiVersions).filter(ApiVersions.name == version_name).first()
            method = db.query(HttpMethods).filter(HttpMethods.name == method_name).first()
            module = db.query(Modules).filter(Modules.name == module_name).first()
            feature = db.query(Features).filter(Features.name == feature_name).first()
            
            if version and method and module and feature:
                module_feature = db.query(ModulesFeatures).filter(
                    ModulesFeatures.module_id == module.id,
                    ModulesFeatures.feature_id == feature.id
                ).first()
                
                if module_feature:
                    permission = Permission(
                        name=perm_name,
                        version_id=version.id,
                        method_id=method.id,
                        module_feature_id=module_feature.id
                    )
                    db.add(permission)
    db.commit()

    # Create roles and assign permissions
    for role_name, role_perms in ROLES.items():
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name, description=f"Rol de {role_name}")
            db.add(role)
            db.commit()
            db.refresh(role)

        for perm_name in role_perms:
            permission = db.query(Permission).filter(Permission.name == perm_name).first()
            if permission and permission not in role.permissions:
                role.permissions.append(permission)
        db.commit()

    # Create default project
    default_project = db.query(Project).filter(Project.name == "Default Project").first()
    if not default_project:
        default_project = Project(name="Default Project")
        db.add(default_project)
        db.commit()
        db.refresh(default_project)

    # Get active status
    active_status = db.query(UserStatus).filter(UserStatus.name == "ACTIVE").first()

    # Create admin user
    admin_user = db.query(User).filter(User.email == settings.ADMIN_USER_EMAIL).first()
    if not admin_user:
        admin_role = db.query(Role).filter(Role.name == "Super Admin").first()
        user_in = UserCreate(
            email=settings.ADMIN_USER_EMAIL,
            full_name="Administrador",
            password=settings.ADMIN_USER_PASSWORD,
            project_id=default_project.id,
            role_ids=[admin_role.id] if admin_role else []
        )
        user_repository.create(db, obj_in=user_in, status_id=active_status.id)

    # Create basic user example
    basic_user = db.query(User).filter(User.email == "user@example.com").first()
    if not basic_user:
        basic_role = db.query(Role).filter(Role.name == "Basic User").first()
        user_in = UserCreate(
            email=settings.BASE_USER_EMAIL,
            full_name="Usuario Básico",
            password=settings.BASE_USER_PASSWORD,
            project_id=default_project.id,
            role_ids=[basic_role.id] if basic_role else []
        )
        user_repository.create(db, obj_in=user_in, status_id=active_status.id)
