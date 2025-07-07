from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from models.invitation import Invitation
from repositories.invitation_repository import InvitationRepository
from repositories.audit_log_repository import AuditLogRepository
from schemas.invitation import InvitationCreate

import logging

class InvitationService:
    def __init__(self, invitation_repo: InvitationRepository, audit_repo: AuditLogRepository, parametric_service=None):
        self.invitation_repo = invitation_repo
        self.audit_repo = audit_repo
        self.parametric_service = parametric_service

    def create_invitation(self, db: Session, invitation_in: InvitationCreate, current_user_id: int) -> Invitation:
        """
        RF 1.4.1: Generar código de invitación
        """
        invitation = self.invitation_repo.create(db, obj_in=invitation_in, created_by_id=current_user_id)
        
        # Log invitation creation
        self.audit_repo.create_log(
            db,
            user_id=current_user_id,
            action="invitacion.generar",
            details={
                "invitation_id": invitation.id,
                "invitation_code": invitation.code,
                "invited_email": invitation.email,
                "roles_assigned": [role.id for role in invitation.roles]
            }
        )
        
        return invitation

    def get_invitations(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[int] = None,
        email_filter: Optional[str] = None,
        role_filter: Optional[int] = None
    ) -> List[Invitation]:
        """
        RF 1.4.2: Consultar y gestionar invitaciones
        """
        # Auto-expire old invitations
        self.invitation_repo.expire_old_invitations(db)
        
        return self.invitation_repo.get_all(
            db,
            skip=skip,
            limit=limit,
            status_filter=status_filter,
            email_filter=email_filter,
            role_filter=role_filter
        )

    def get_invitation_by_id(self, db: Session, invitation_id: int) -> Invitation:
        """
        Ver detalles de una invitación específica
        """
        invitation = self.invitation_repo.get_by_id(db, id=invitation_id)
        if not invitation:
            logging.error(f"Invitation not found: {invitation_id}")
            raise HTTPException(status_code=404, detail="Invitation not found")
        return invitation

    def cancel_invitation(self, db: Session, invitation_id: int, current_user_id: int) -> Invitation:
        """
        RF 1.4.2: Cancelar invitación
        """
        invitation = self.invitation_repo.get_by_id(db, id=invitation_id)
        if not invitation:
            logging.error(f"Invitation not found: {invitation_id}")
            raise HTTPException(status_code=404, detail="Invitation not found")
        
        # Check invitation status using parametric service
        if self.parametric_service:
            pending_status = self.parametric_service.get_pending_invitation_status(db)
            if invitation.status_id != pending_status.id:
                logging.error(f"Invitation is not pending: {invitation_id}")
                raise HTTPException(status_code=400, detail="Only pending invitations can be cancelled")
        else:
            # Fallback to direct relationship access
            if invitation.status.name != "PENDING":
                logging.error(f"Invitation is not pending: {invitation_id}")
                raise HTTPException(status_code=400, detail="Only pending invitations can be cancelled")
        
        cancelled_invitation = self.invitation_repo.cancel(db, id=invitation_id)
        
        # Log invitation cancellation
        self.audit_repo.create_log(
            db,
            user_id=current_user_id,
            action="invitacion.cancelar",
            details={
                "invitation_id": invitation_id,
                "invitation_code": invitation.code,
                "invited_email": invitation.email
            }
        )
        
        return cancelled_invitation

    def validate_invitation_for_registration(self, db: Session, code: str, email: str) -> Invitation:
        """
        RF 2.5.2: Validar invitación para registro
        """
        # Validate invitation code
        invitation = self.invitation_repo.get_by_code(db, code=code)
        if not invitation:
            logging.error(f"Invalid invitation code: {code}")
            raise HTTPException(status_code=400, detail="Invalid invitation code")
        
        # Check invitation status using parametric service
        if self.parametric_service:
            pending_status = self.parametric_service.get_pending_invitation_status(db)
            if invitation.status_id != pending_status.id:
                logging.error(f"Invitation is not pending: {code}")
                raise HTTPException(status_code=400, detail="Invitation code has already been used or is no longer valid")
        else:
            # Fallback to direct relationship access
            if invitation.status.name != "PENDING":
                logging.error(f"Invitation is not pending: {code}")
                raise HTTPException(status_code=400, detail="Invitation code has already been used or is no longer valid")
        
        # Check expiration
        if invitation.expires_at < datetime.utcnow():
            logging.error(f"Invitation has expired: {code}")
            raise HTTPException(status_code=400, detail="Invitation code has expired")
        
        # Validate email matches invitation
        if email != invitation.email:
            logging.error(f"Email does not match invitation: {email}")
            raise HTTPException(status_code=400, detail="Email does not match invitation")
        
        return invitation

    def accept_invitation(self, db: Session, code: str) -> Invitation:
        """
        Marcar invitación como aceptada
        """
        return self.invitation_repo.accept(db, code=code)

    def validate_invitation_code(self, db: Session, invitation_code: str) -> Invitation:
        """
        RF 2.5: Validar código de invitación (público)
        Valida si un código de invitación es válido
        """
        invitation = self.invitation_repo.get_by_code(db, code=invitation_code)
        if not invitation:
            logging.error(f"Invalid invitation code: {invitation_code}")
            raise HTTPException(status_code=404, detail="Invalid invitation code")
        
        # For now, just return the invitation if found
        # Additional validations can be added later if needed
        return invitation 