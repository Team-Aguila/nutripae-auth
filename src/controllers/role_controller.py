from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging
from db.session import get_db
from schemas.role import Role, RoleCreate, RoleUpdate, RoleWithUsers
from schemas.user import UserListItem
from services.role_service import RoleService
from core.service_dependencies import get_role_service
from core.dependencies import require_permissions, get_current_active_user
from models.user import User as UserModel

router = APIRouter()

@router.post("/", response_model=Role, status_code=201)
def create_role(
    *,
    db: Session = Depends(get_db),
    role_in: RoleCreate,
    current_user: UserModel = Depends(get_current_active_user),
    role_service: RoleService = Depends(get_role_service),
    _: dict = Depends(require_permissions(["role:create"]))
):
    logging.info(f"Creating role: {role_in.name}")
    """
    RF 1.2.1: Crear nuevo rol
    Interfaz accesible para usuarios con permiso 'role:create'
    """
    return role_service.create_role(db, role_in, current_user.id)

@router.get("/", response_model=List[RoleWithUsers])
def list_roles(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    role_service: RoleService = Depends(get_role_service),
    _: dict = Depends(require_permissions(["role:list"]))
):
    logging.info(f"Listing roles")
    """
    RF 1.2.2: Consultar roles
    Muestra un listado paginado de todos los roles definidos
    """
    roles_with_count = role_service.get_roles(db, skip=skip, limit=limit)
    
    # Convert to RoleWithUsers format
    result = []
    for role_data in roles_with_count:
        role_with_users = RoleWithUsers(
            id=role_data['id'],
            name=role_data['name'],
            description=role_data['description'],
            user_count=role_data['user_count'],
            permissions=role_data['permissions']
        )
        result.append(role_with_users)
    
    return result

@router.get("/{role_id}", response_model=Role)
def get_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    role_service: RoleService = Depends(get_role_service),
    _: dict = Depends(require_permissions(["role:read"]))
):
    logging.info(f"Getting role by id: {role_id}")
    """
    RF 1.2.3: Consultar detalle de rol
    Muestra toda la información de un rol específico
    """
    return role_service.get_role_by_id(db, role_id)

@router.get("/{role_id}/users", response_model=List[UserListItem])
def get_role_users(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UserModel = Depends(get_current_active_user),
    role_service: RoleService = Depends(get_role_service),
    _: dict = Depends(require_permissions(["role:read"]))
):
    logging.info(f"Getting users by role: {role_id}")
    """
    RF 1.2.3: Usuarios asignados a un rol
    Lista los usuarios que tienen asignado un rol específico
    """
    return role_service.get_role_users(db, role_id, skip=skip, limit=limit)

@router.put("/{role_id}", response_model=Role)
def update_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    role_in: RoleUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    role_service: RoleService = Depends(get_role_service),
    _: dict = Depends(require_permissions(["role:update"]))
):
    logging.info(f"Updating role: {role_id}")
    """
    RF 1.2.4: Modificar rol
    Permite editar un rol y sus permisos asociados
    """
    return role_service.update_role(db, role_id, role_in, current_user.id)

@router.delete("/{role_id}", response_model=Role)
def delete_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    role_service: RoleService = Depends(get_role_service),
    _: dict = Depends(require_permissions(["role:delete"]))
):
    logging.info(f"Deleting role: {role_id}")
    """
    RF 1.2.5: Eliminar rol
    Elimina un rol si no tiene usuarios asignados
    """
    return role_service.delete_role(db, role_id, current_user.id) 