from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from typing import List, Optional
from datetime import datetime
from core.security import get_password_hash
from models.user import User
from models.role import Role
from models.parametric import UserStatus
from schemas.user import UserCreate, UserUpdate
import logging
class UserRepository:
    def get_by_email(self, db: Session, *, email: str) -> User | None:
        logging.info(f"Getting user by email: {email}")
        return db.query(User).options(joinedload(User.roles), joinedload(User.project)).filter(User.email == email).first()
    
    def get_by_id(self, db: Session, *, id: int) -> User | None:
        logging.info(f"Getting user by id: {id}")
        return db.query(User).options(joinedload(User.roles), joinedload(User.project)).filter(User.id == id).first()
    
    def get_by_username(self, db: Session, *, username: str) -> User | None:
        logging.info(f"Getting user by username: {username}")
        return db.query(User).options(joinedload(User.roles), joinedload(User.project)).filter(User.username == username).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100, 
                status_filter: Optional[int] = None,
                role_filter: Optional[int] = None,
                search: Optional[str] = None) -> List[User]:
        logging.info(f"Getting all users with filters: status_filter={status_filter}, role_filter={role_filter}, search={search}")
        query = db.query(User).options(joinedload(User.roles), joinedload(User.project))
        
        if status_filter:
            query = query.filter(User.status_id == status_filter)
        
        if role_filter:
            query = query.join(User.roles).filter(Role.id == role_filter)
        
        if search:
            query = query.filter(
                or_(
                    User.full_name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%")
                )
            )
        
        # Excluir usuarios eliminados lógicamente por defecto
        query = query.filter(User.deleted_at.is_(None))
        
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: UserCreate, status_id: int) -> User:
        logging.info(f"Creating user: {obj_in.email}")
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            full_name=obj_in.full_name,
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=hashed_password,
            phone_number=obj_in.phone_number,
            project_id=obj_in.project_id,
            status_id=status_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Asignar roles
        if obj_in.role_ids:
            roles = db.query(Role).filter(Role.id.in_(obj_in.role_ids)).all()
            db_obj.roles.extend(roles)
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        logging.info(f"Updating user: {db_obj.id}")
        update_data = obj_in.dict(exclude_unset=True)
        
        # Manejar roles por separado
        role_ids = update_data.pop('role_ids', None)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        if role_ids is not None:
            # Limpiar roles existentes
            db_obj.roles.clear()
            # Asignar nuevos roles
            if role_ids:
                roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
                db_obj.roles.extend(roles)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_password(self, db: Session, *, user: User, new_password: str) -> User:
        logging.info(f"Updating password for user: {user.id}")
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
        return user
    
    def update_last_login(self, db: Session, *, user: User) -> User:
        logging.info(f"Updating last login for user: {user.id}")
        user.last_login_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    def delete_logical(self, db: Session, *, id: int) -> User | None:
        logging.info(f"Deleting user logically: {id}")
        db_obj = self.get_by_id(db, id=id)
        if db_obj:
            db_obj.deleted_at = datetime.utcnow()
            # Cambiar estado a DELETED
            deleted_status = db.query(UserStatus).filter(UserStatus.name == "DELETED").first()
            if deleted_status:
                db_obj.status_id = deleted_status.id
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def count_by_status(self, db: Session, status_id: int) -> int:
        logging.info(f"Counting users by status: {status_id}")
        return db.query(User).filter(User.status_id == status_id, User.deleted_at.is_(None)).count()

user_repository = UserRepository()
