from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from db.session import get_db
from core.dependencies import get_current_user
from schemas.token import TokenData
from repositories.user_repository import user_repository
import logging

router = APIRouter()

class AuthorizationRequest(BaseModel):
    endpoint: str
    method: str
    required_permissions: List[str] = []

class AuthorizationResponse(BaseModel):
    authorized: bool
    user_id: int | None = None
    user_email: str | None = None
    user_permissions: List[str] = []
    required_permissions: List[str] = []
    missing_permissions: List[str] = []
    endpoint: str
    method: str

@router.post("/check-authorization", response_model=AuthorizationResponse)
def check_user_authorization(
    *,
    db: Session = Depends(get_db),
    request: AuthorizationRequest,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Endpoint de autorización externa para otros módulos
    
    Valida si un usuario tiene los permisos necesarios para acceder a un endpoint específico.
    Este endpoint es el ÚNICO responsable de toda la lógica de autorización.
    
    Args:
        request: Contiene endpoint, método HTTP y permisos requeridos
        current_user: Datos del usuario extraídos del JWT
        
    Returns:
        AuthorizationResponse: Información completa de autorización
    """
    try:
        # Verificar que el usuario existe y está activo en la base de datos
        user = user_repository.get_by_email(db, email=current_user.email)
        if not user:
            logging.error(f"User not found in database: {current_user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found in database"
            )
        
        if user.status.name != "ACTIVE" or user.deleted_at:
            logging.error(f"User account is not active: {current_user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is not active"
            )
        
        # Obtener permisos del usuario del token JWT
        user_permissions = set(current_user.permissions)
        required_perms_set = set(request.required_permissions)
        logging.info(f"User permissions: {user_permissions}")
        logging.info(f"Required permissions: {required_perms_set}")
        # Calcular permisos faltantes
        missing_permissions = list(required_perms_set - user_permissions)
        logging.info(f"Missing permissions: {missing_permissions}")
        # Usuario está autorizado si tiene todos los permisos requeridos
        authorized = len(missing_permissions) == 0
        logging.info(f"Authorized: {authorized}")
        # Crear respuesta completa
        response = AuthorizationResponse(
            authorized=authorized,
            user_id=current_user.user_id,
            user_email=current_user.email,
            user_permissions=list(user_permissions),
            required_permissions=request.required_permissions,
            missing_permissions=missing_permissions,
            endpoint=request.endpoint,
            method=request.method
        )
        logging.info(f"Response: {response}")
        return response
        
    except HTTPException:
        # Re-lanzar HTTPExceptions tal como están
        logging.error(f"HTTPException: {e}")
        raise
    except Exception as e:
        # Cualquier otro error se convierte en 500
        logging.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing authorization request: {str(e)}"
        )

@router.get("/user-permissions")
def get_user_permissions(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    """
    Obtiene todos los permisos del usuario actual
    
    Útil para que otros módulos puedan consultar todos los permisos
    de un usuario sin necesidad de verificar permisos específicos.
    """
    try:
        # Verificar que el usuario existe y está activo
        user = user_repository.get_by_email(db, email=current_user.email)
        if not user:
            logging.error(f"User not found in database: {current_user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found in database"
            )
        
        if user.status.name != "ACTIVE" or user.deleted_at:
            logging.error(f"User account is not active: {current_user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is not active"
            )
        logging.info(f"User found: {current_user.email}")
        return {
            "user_id": current_user.user_id,
            "user_email": current_user.email,
            "role": current_user.role,
            "project_id": current_user.project_id,
            "permissions": current_user.permissions
        }
        
    except HTTPException:
        logging.error(f"HTTPException: {e}")
        raise
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user permissions: {str(e)}"
        ) 