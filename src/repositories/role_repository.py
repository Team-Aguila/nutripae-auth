from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from models.role import Role
from models.permission import Permission
from models.user import User
from schemas.role import RoleCreate, RoleUpdate
import logging

class RoleRepository:
    def get_by_id(self, db: Session, *, id: int) -> Role | None:
        logging.info(f"Getting role by id: {id}")
        return db.query(Role).options(joinedload(Role.permissions)).filter(Role.id == id).first()

    def get_by_name(self, db: Session, *, name: str) -> Role | None:
        logging.info(f"Getting role by name: {name}")
        return db.query(Role).options(joinedload(Role.permissions)).filter(Role.name == name).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
        logging.info("Getting all roles")
        return db.query(Role).options(joinedload(Role.permissions)).offset(skip).limit(limit).all()
    
    def get_all_with_user_count(self, db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get roles with user count"""
        logging.info("Getting roles with user count")
        roles_with_count = db.query(
            Role,
            func.count(User.id).label('user_count')
        ).outerjoin(
            User, Role.users
        ).group_by(Role.id).offset(skip).limit(limit).all()
        
        result = []
        for role, count in roles_with_count:
            role_dict = {
                'id': role.id,
                'name': role.name,
                'description': role.description,
                'user_count': count or 0,
                'permissions': role.permissions
            }
            result.append(role_dict)
        
        return result

    def create(self, db: Session, *, obj_in: RoleCreate) -> Role:
        logging.info(f"Creating role: {obj_in.name}")
        db_obj = Role(name=obj_in.name, description=obj_in.description)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Assign permissions
        if obj_in.permission_ids:
            permissions = db.query(Permission).filter(Permission.id.in_(obj_in.permission_ids)).all()
            db_obj.permissions.extend(permissions)
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

    def update(self, db: Session, *, db_obj: Role, obj_in: RoleUpdate) -> Role:
        logging.info(f"Updating role: {db_obj.id}")
        update_data = obj_in.dict(exclude_unset=True)
        
        # Handle permissions separately
        permission_ids = update_data.pop('permission_ids', None)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        if permission_ids is not None:
            # Clear existing permissions
            db_obj.permissions.clear()
            # Assign new permissions
            if permission_ids:
                permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
                db_obj.permissions.extend(permissions)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Role | None:
        logging.info(f"Deleting role: {id}")
        db_obj = self.get_by_id(db, id=id)
        if db_obj:
            # Check if role has users assigned
            user_count = db.query(User).join(User.roles).filter(Role.id == id).count()
            if user_count > 0:
                raise ValueError(f"Cannot delete role '{db_obj.name}' because it has {user_count} users assigned. Please reassign users first.")
            
            db.delete(db_obj)
            db.commit()
        return db_obj

    def get_users_by_role(self, db: Session, *, role_id: int, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users assigned to a specific role"""
        logging.info(f"Getting users assigned to role: {role_id}")
        return db.query(User).join(User.roles).filter(Role.id == role_id).offset(skip).limit(limit).all()

role_repository = RoleRepository()
