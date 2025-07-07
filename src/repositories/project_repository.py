from sqlalchemy.orm import Session
from datetime import datetime
from models.project import Project
from schemas.project import ProjectCreate
import logging
class ProjectRepository:
    def get(self, db: Session, id: int) -> Project | None:
        logging.info(f"Getting project by id: {id}")
        return db.query(Project).filter(Project.id == id, Project.deleted_at == None).first()

    def get_all(self, db: Session) -> list[Project]:
        logging.info("Getting all projects")
        return db.query(Project).filter(Project.deleted_at == None).all()

    def create(self, db: Session, *, obj_in: ProjectCreate) -> Project:
        logging.info(f"Creating project: {obj_in.name}")
        db_obj = Project(name=obj_in.name, logo_url=obj_in.logo_url)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Project, obj_in: dict) -> Project:
        logging.info(f"Updating project: {db_obj.id}")
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Project | None:
        logging.info(f"Removing project: {id}")
        db_obj = self.get(db, id)
        if db_obj:
            db_obj.deleted_at = datetime.utcnow()
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

project_repository = ProjectRepository()
