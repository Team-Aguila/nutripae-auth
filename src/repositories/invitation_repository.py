from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
import string
from models.invitation import Invitation
from models.role import Role
from models.parametric import InvitationStatus
from schemas.invitation import InvitationCreate, InvitationUpdate
import logging
class InvitationRepository:
    def generate_invitation_code(self) -> str:
        """Generate a unique 10-character invitation code"""
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(10))
    
    def get_by_id(self, db: Session, *, id: int) -> Invitation | None:
        logging.info(f"Getting invitation by id: {id}")
        return db.query(Invitation).options(joinedload(Invitation.roles)).filter(Invitation.id == id).first()
    
    def get_by_code(self, db: Session, *, code: str) -> Invitation | None:
        logging.info(f"Getting invitation by code: {code}")
        return db.query(Invitation).options(joinedload(Invitation.roles)).filter(Invitation.code == code).first()
    
    def get_by_email(self, db: Session, *, email: str) -> List[Invitation]:
        logging.info(f"Getting invitations by email: {email}")
        return db.query(Invitation).options(joinedload(Invitation.roles)).filter(Invitation.email == email).all()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100,
                status_filter: Optional[int] = None,
                email_filter: Optional[str] = None,
                role_filter: Optional[int] = None) -> List[Invitation]:
        logging.info(f"Getting invitations with status: {status_filter}, email: {email_filter}, role: {role_filter}")
        query = db.query(Invitation).options(joinedload(Invitation.roles))
        
        if status_filter:
            query = query.filter(Invitation.status_id == status_filter)
        
        if email_filter:
            query = query.filter(Invitation.email.ilike(f"%{email_filter}%"))
        
        if role_filter:
            query = query.join(Invitation.roles).filter(Role.id == role_filter)
        
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: InvitationCreate, created_by_id: int) -> Invitation:
        logging.info(f"Creating invitation for email: {obj_in.email}")
        # Generate unique code
        code = self.generate_invitation_code()
        while self.get_by_code(db, code=code):
            code = self.generate_invitation_code()
        
        # Set expiration date (default 7 days)
        expires_at = obj_in.expires_at or datetime.utcnow() + timedelta(days=7)
        
        # Get PENDING status
        pending_status = db.query(InvitationStatus).filter(InvitationStatus.name == "PENDING").first()
        
        db_obj = Invitation(
            code=code,
            email=obj_in.email,
            status_id=pending_status.id,
            expires_at=expires_at,
            created_by_id=created_by_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Assign roles
        if obj_in.role_ids:
            roles = db.query(Role).filter(Role.id.in_(obj_in.role_ids)).all()
            db_obj.roles.extend(roles)
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

    def update(self, db: Session, *, db_obj: Invitation, obj_in: InvitationUpdate) -> Invitation:
        logging.info(f"Updating invitation: {db_obj.id}")
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def cancel(self, db: Session, *, id: int) -> Invitation | None:
        logging.info(f"Cancelling invitation: {id}")
        db_obj = self.get_by_id(db, id=id)
        if db_obj:
            cancelled_status = db.query(InvitationStatus).filter(InvitationStatus.name == "CANCELLED").first()
            if cancelled_status:
                db_obj.status_id = cancelled_status.id
                db.commit()
                db.refresh(db_obj)
        return db_obj

    def accept(self, db: Session, *, code: str) -> Invitation | None:
        logging.info(f"Accepting invitation: {code}")
        db_obj = self.get_by_code(db, code=code)
        if db_obj:
            accepted_status = db.query(InvitationStatus).filter(InvitationStatus.name == "ACCEPTED").first()
            if accepted_status:
                db_obj.status_id = accepted_status.id
                db.commit()
                db.refresh(db_obj)
        return db_obj

    def expire_old_invitations(self, db: Session) -> int:
        logging.info("Expiring old invitations")
        """Mark expired invitations as EXPIRED"""
        expired_status = db.query(InvitationStatus).filter(InvitationStatus.name == "EXPIRED").first()
        pending_status = db.query(InvitationStatus).filter(InvitationStatus.name == "PENDING").first()
        
        if not expired_status or not pending_status:
            return 0
        
        expired_invitations = db.query(Invitation).filter(
            and_(
                Invitation.status_id == pending_status.id,
                Invitation.expires_at < datetime.utcnow()
            )
        ).all()
        
        count = 0
        for invitation in expired_invitations:
            invitation.status_id = expired_status.id
            count += 1
        
        db.commit()
        return count

invitation_repository = InvitationRepository() 