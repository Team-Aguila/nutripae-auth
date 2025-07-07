from typing import List, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging
from models.role import Role
from models.user import User
from repositories.role_repository import RoleRepository
from repositories.audit_log_repository import AuditLogRepository
from schemas.role import RoleCreate, RoleUpdate


class RoleService:
    def __init__(self, role_repo: RoleRepository, audit_repo: AuditLogRepository):
        self.role_repo = role_repo
        self.audit_repo = audit_repo

    def create_role(self, db: Session, role_in: RoleCreate, current_user_id: int) -> Role:
        """
        RF 1.2.1: Crear nuevo rol
        """
        # Check if role name already exists
        existing_role = self.role_repo.get_by_name(db, name=role_in.name)
        if existing_role:
            logging.error(f"Role name already exists: {role_in.name}")
            raise HTTPException(status_code=400, detail="Role name already exists")
        
        # Create role
        role = self.role_repo.create(db, obj_in=role_in)
        
        # Log role creation
        self.audit_repo.create_log(
            db,
            user_id=current_user_id,
            action="rol.crear",
            details={
                "role_id": role.id,
                "role_name": role.name,
                "permissions_assigned": [p.id for p in role.permissions]
            }
        )
        
        return role

    def get_roles(self, db: Session, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        RF 1.2.2: Consultar roles
        """
        return self.role_repo.get_all_with_user_count(db, skip=skip, limit=limit)

    def get_role_by_id(self, db: Session, role_id: int) -> Role:
        """
        RF 1.2.3: Consultar detalle de rol
        """
        role = self.role_repo.get_by_id(db, id=role_id)
        if not role:
            logging.error(f"Role not found: {role_id}")
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    def get_role_users(self, db: Session, role_id: int, skip: int = 0, limit: int = 100) -> List[User]:
        """
        RF 1.2.3: Usuarios asignados a un rol
        """
        role = self.role_repo.get_by_id(db, id=role_id)
        if not role:
            logging.error(f"Role not found: {role_id}")
            raise HTTPException(status_code=404, detail="Role not found")
        
        return self.role_repo.get_users_by_role(db, role_id=role_id, skip=skip, limit=limit)

    def update_role(self, db: Session, role_id: int, role_in: RoleUpdate, current_user_id: int) -> Role:
        """
        RF 1.2.4: Modificar rol
        """
        role = self.role_repo.get_by_id(db, id=role_id)
        if not role:
            logging.error(f"Role not found: {role_id}")
            raise HTTPException(status_code=404, detail="Role not found")
        
        # Check name uniqueness if name is being changed
        update_data = role_in.dict(exclude_unset=True)
        if "name" in update_data and update_data["name"] != role.name:
            existing_role = self.role_repo.get_by_name(db, name=update_data["name"])
            if existing_role and existing_role.id != role_id:
                logging.error(f"Role name already exists: {update_data['name']}")
                raise HTTPException(status_code=400, detail="Role name already exists")
        
        # Store old values for audit
        old_permissions = [p.id for p in role.permissions]
        
        # Update role
        updated_role = self.role_repo.update(db, db_obj=role, obj_in=role_in)
        
        # Log role update
        new_permissions = [p.id for p in updated_role.permissions]
        
        self.audit_repo.create_log(
            db,
            user_id=current_user_id,
            action="rol.editar",
            details={
                "role_id": role_id,
                "role_name": updated_role.name,
                "old_permissions": old_permissions,
                "new_permissions": new_permissions
            }
        )
        
        return updated_role

    def delete_role(self, db: Session, role_id: int, current_user_id: int) -> Role:
        """
        RF 1.2.5: Eliminar rol
        """
        role = self.role_repo.get_by_id(db, id=role_id)
        if not role:
            logging.error(f"Role not found: {role_id}")
            raise HTTPException(status_code=404, detail="Role not found")
        
        try:
            deleted_role = self.role_repo.delete(db, id=role_id)
            
            # Log role deletion
            self.audit_repo.create_log(
                db,
                user_id=current_user_id,
                action="rol.eliminar",
                details={
                    "role_id": role_id,
                    "role_name": role.name
                }
            )
            
            return deleted_role
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) 