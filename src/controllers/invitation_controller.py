from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.invitation import Invitation, InvitationCreate, InvitationListItem
from services.invitation_service import InvitationService
from core.service_dependencies import get_invitation_service
from core.dependencies import require_permissions, get_current_active_user
from models.user import User as UserModel
import logging
router = APIRouter()

@router.post("/", response_model=Invitation, status_code=201)
def create_invitation(
    *,
    db: Session = Depends(get_db),
    invitation_in: InvitationCreate,
    current_user: UserModel = Depends(get_current_active_user),
    invitation_service: InvitationService = Depends(get_invitation_service),
    _: dict = Depends(require_permissions(["invitation:create"]))
):
    """
    RF 1.4.1: Generar código de invitación
    Genera un código único para invitar a un nuevo usuario
    """
    logging.info(f"Creating invitation for user: {current_user.email}")
    return invitation_service.create_invitation(db, invitation_in, current_user.id)

@router.get("/", response_model=List[InvitationListItem])
def list_invitations(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status_filter: Optional[int] = Query(None, description="Filter by status ID"),
    email_filter: Optional[str] = Query(None, description="Filter by email"),
    role_filter: Optional[int] = Query(None, description="Filter by role ID"),
    current_user: UserModel = Depends(get_current_active_user),
    invitation_service: InvitationService = Depends(get_invitation_service),
    _: dict = Depends(require_permissions(["invitation:list"]))
):
    """
    RF 1.4.2: Consultar y gestionar invitaciones
    Muestra un listado paginado y filtrable de las invitaciones generadas
    """
    logging.info(f"Listing invitations for user: {current_user.email}")
    return invitation_service.get_invitations(
        db,
        skip=skip,
        limit=limit,
        status_filter=status_filter,
        email_filter=email_filter,
        role_filter=role_filter
    )

@router.get("/{invitation_id}", response_model=Invitation)
def get_invitation(
    *,
    db: Session = Depends(get_db),
    invitation_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    invitation_service: InvitationService = Depends(get_invitation_service),
    _: dict = Depends(require_permissions(["invitation:list"]))
):
    """
    Ver detalles de una invitación específica
    """
    logging.info(f"Getting invitation by id: {invitation_id}")
    return invitation_service.get_invitation_by_id(db, invitation_id)

@router.put("/{invitation_id}/cancel", response_model=Invitation)
def cancel_invitation(
    *,
    db: Session = Depends(get_db),
    invitation_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    invitation_service: InvitationService = Depends(get_invitation_service),
    _: dict = Depends(require_permissions(["invitation:create"]))
):
    """
    RF 1.4.2: Cancelar invitación
    Cambia el estado de una invitación a cancelada
    """
    logging.info(f"Cancelling invitation: {invitation_id}")
    return invitation_service.cancel_invitation(db, invitation_id, current_user.id)

# Public endpoints for invitation validation and usage
@router.get("/validate/{invitation_code}")
def validate_invitation_code(
    *,
    db: Session = Depends(get_db),
    invitation_code: str,
    invitation_service: InvitationService = Depends(get_invitation_service)
):
    """
    RF 2.5: Validar código de invitación (público)
    Valida si un código de invitación es válido sin requerir autenticación
    """
    logging.info(f"Validating invitation code: {invitation_code}")
    try:
        invitation = invitation_service.validate_invitation_code(db, invitation_code)
        return {
            "valid": True,
            "invitation": {
                "email": invitation.email,
                "expires_at": invitation.expires_at,
                "roles": [{"id": role.id, "name": role.name} for role in invitation.roles]
            }
        }
    except Exception as e:
        logging.error(f"Exception: {e}")
        return {"valid": False, "message": "Invalid invitation code"} 