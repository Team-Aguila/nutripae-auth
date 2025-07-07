from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
import logging
from db.session import get_db
from schemas.user import User, UserCreate, PasswordChange, UserLogin
from schemas.token import Token, TokenData
from services.auth_service import AuthService
from services.invitation_service import InvitationService
from core.service_dependencies import get_auth_service, get_invitation_service
from repositories.user_repository import user_repository
from repositories.audit_log_repository import audit_log_repository
from core.dependencies import require_permissions, get_current_user

router = APIRouter()

@router.post("/register", response_model=User, status_code=201)
def register(
    user: UserCreate, 
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Crea un nuevo usuario. Abierto al público.
    En una app real, podrías querer proteger esto o añadir captchas.
    """
    return auth_service.register_user(db=db, user_in=user)

@router.post("/register-by-invitation", response_model=User, status_code=201)
def register_by_invitation(
    *,
    db: Session = Depends(get_db),
    invitation_code: str,
    user_data: dict,  # Contains: email, full_name, username, password, confirm_password
    auth_service: AuthService = Depends(get_auth_service),
    invitation_service: InvitationService = Depends(get_invitation_service)
):
    """
    RF 2.5: Proceso de registro mediante canje de código de invitación
    Permite registrarse usando un código de invitación válido
    """
    # Validate password confirmation
    if user_data["password"] != user_data.get("confirm_password"):
        logging.error("Passwords do not match")
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Validate invitation
    logging.info(f"Validating invitation for registration: {invitation_code}")
    invitation = invitation_service.validate_invitation_for_registration(
        db, 
        invitation_code, 
        user_data["email"]
    )
    logging.info(f"Invitation validated: {invitation}")
    # Create user
    logging.info(f"Creating user: {user_data['email']}")
    user_create = UserCreate(
        email=user_data["email"],
        full_name=user_data["full_name"],
        username=user_data.get("username"),
        password=user_data["password"],
        role_ids=[role.id for role in invitation.roles]
    )
    logging.info(f"User created: {user_create}")
    try:
        logging.info(f"Accepting invitation: {invitation_code}")
        new_user = auth_service.register_user_by_invitation(
            db, 
            user_create, 
            invitation.id
        )
        
        # Mark invitation as accepted
        invitation_service.accept_invitation(db, invitation_code)
        logging.info(f"Invitation accepted: {invitation_code}")
        return new_user
    except HTTPException:
        logging.error(f"HTTPException: {e}")
        raise
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Autentica a un usuario y devuelve un token JWT.
    """
    user = auth_service.authenticate_user(db, email=login_data.email, password=login_data.password)
    if not user:
        logging.error("User not found")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logging.info(f"User authenticated: {user.email}")
    return auth_service.create_access_token(user=user)

@router.post("/forgot-password")
def forgot_password(
    *,
    db: Session = Depends(get_db),
    email: str,
):
    """
    RF 2.2.1: Solicitar restablecimiento de contraseña
    Envía un email con token para restablecer contraseña
    """
    # Check if user exists and is active
    user = user_repository.get_by_email(db, email=email)
    logging.info(f"User found: {user}")
    # Always return success for security (don't reveal if email exists)
    if user and user.status.name == "ACTIVE" and not user.deleted_at:
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        logging.info(f"Reset token generated: {reset_token}")
        # Store token in cache/database (simplified - in real app use Redis or DB table)
        # For now, just log it
        audit_log_repository.create_log(
            db,
            user_id=user.id,
            action="password.reset_requested",
            details={
                "email": email,
                "reset_token": reset_token,
                "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat()
            }
        )
        logging.info(f"Audit log created: {reset_token}")
        # In real implementation, send email with reset link
        # background_tasks.add_task(send_reset_email, email, reset_token)
    
    return {"message": "If the email exists, you will receive password reset instructions"}

@router.post("/reset-password")
def reset_password(
    *,
    db: Session = Depends(get_db),
    reset_token: str,
    new_password: str,
    confirm_password: str
):
    """
    RF 2.2.2: Restablecer contraseña
    Restablece la contraseña usando un token válido
    """
    logging.info(f"Resetting password for token: {reset_token}")
    if new_password != confirm_password:
        logging.error("Passwords do not match")
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    logging.info(f"Validating reset token: {reset_token}")
    # In real implementation, validate token from cache/database
    # For now, return error since we don't have token storage
    logging.error("Invalid or expired reset token")
    raise HTTPException(status_code=400, detail="Invalid or expired reset token")

@router.post("/change-password")
def change_password(
    passwords: PasswordChange,
    db: Session = Depends(get_db),
    current_user_data: TokenData = Depends(require_permissions(["user:update_own"])),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Permite a un usuario cambiar su propia contraseña.
    Requiere el permiso 'user:update_own'.
    """
    logging.info(f"Changing password for user: {current_user_data.email}")
    user = user_repository.get_by_email(db, email=current_user_data.email)
    if not user:
        logging.error(f"User not found: {current_user_data.email}")
        raise HTTPException(status_code=404, detail="User not found")
    logging.info(f"User found: {user.email}")
    auth_service.change_password(db, user, passwords.old_password, passwords.new_password)
    logging.info(f"Password changed for user: {user.email}")
    return {"message": "Password changed successfully"}

@router.get("/me", response_model=User)
def read_users_me(
    db: Session = Depends(get_db),
    current_user_data: TokenData = Depends(require_permissions(["user:read_own"]))
):
    """
    Obtiene la información del usuario actual.
    Requiere el permiso 'user:read_own'.
    """
    logging.info(f"Reading user me: {current_user_data.email}")
    user = user_repository.get_by_email(db, email=current_user_data.email)
    if not user:
        logging.error(f"User not found: {current_user_data.email}")
        raise HTTPException(status_code=404, detail="User not found")
    logging.info(f"User found: {user.email}")
    return user
