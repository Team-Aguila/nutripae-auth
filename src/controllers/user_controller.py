from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.user import User, UserCreate, UserUpdate, UserListItem
from services.user_service import UserService
from core.service_dependencies import get_user_service
from core.dependencies import require_permissions, get_current_active_user
from models.user import User as UserModel
import logging
router = APIRouter()

@router.post("/", response_model=User, status_code=201)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: UserModel = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service),
    _: dict = Depends(require_permissions(["user:create"]))
):
    """
    RF 1.1.1: Crear nuevo usuario
    Interfaz accesible para usuarios con permiso 'user:create'
    """
    logging.info(f"Creating user: {user_in.email}")
    return user_service.create_user(db, user_in, current_user.id)

@router.get("/", response_model=List[UserListItem])
def list_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    status_filter: Optional[int] = Query(None, description="Filter by status ID"),
    role_filter: Optional[int] = Query(None, description="Filter by role ID"),
    search: Optional[str] = Query(None, description="Search by name, email or username"),
    current_user: UserModel = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service),
    _: dict = Depends(require_permissions(["user:list"]))
):
    """
    RF 1.1.5: Listado de usuarios
    Muestra una lista paginada y filtrable de los usuarios registrados
    """
    logging.info(f"Listing users")
    return user_service.get_users(
        db,
        skip=skip,
        limit=limit,
        status_filter=status_filter,
        role_filter=role_filter,
        search=search
    )

@router.get("/{user_id}", response_model=User)
def get_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service),
    _: dict = Depends(require_permissions(["user:read"]))
):
    """
    RF 1.1.2: Consultar detalles de usuario
    Muestra toda la información de un usuario específico
    """
    logging.info(f"Getting user by id: {user_id}")
    return user_service.get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service),
    _: dict = Depends(require_permissions(["user:update"]))
):
    """
    RF 1.1.3: Modificar datos de usuario
    Permite editar la información de un usuario existente
    """
    logging.info(f"Updating user: {user_id}")
    return user_service.update_user(db, user_id, user_in, current_user.id)

@router.delete("/{user_id}", response_model=User)
def delete_user_logical(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service),
    _: dict = Depends(require_permissions(["user:delete"]))
):
    """
    RF 1.1.4: Eliminación lógica de usuario
    Marca un usuario como eliminado lógicamente
    """
    logging.info(f"Deleting user: {user_id}")
    return user_service.delete_user_logical(db, user_id, current_user.id) 