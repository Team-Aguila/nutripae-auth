from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from db.session import get_db
from schemas.project import Project, ProjectCreate
from repositories.project_repository import project_repository
from core.dependencies import require_permissions

router = APIRouter()

@router.post("/", response_model=Project, status_code=201)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate,
    current_user: dict = Depends(require_permissions(["project:create"])) # Asumiendo que TokenData es un dict-like
):
    logging.info(f"Creating project: {project_in.name}")
    return project_repository.create(db=db, obj_in=project_in)

@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permissions(["project:read"]))
):
    logging.info(f"Listing projects")
    return project_repository.get_all(db=db)

@router.get("/{id}", response_model=Project)
def get_project_by_id(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: dict = Depends(require_permissions(["project:read"]))
):
    logging.info(f"Getting project by id: {id}")
    project = project_repository.get(db=db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(get_db),
    id: int,
    project_in: dict, # ProjectUpdate
    current_user: dict = Depends(require_permissions(["project:update"]))
):
    logging.info(f"Updating project: {id}")
    project = project_repository.get(db=db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_repository.update(db=db, db_obj=project, obj_in=project_in)

@router.delete("/{id}")
def delete_project(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: dict = Depends(require_permissions(["project:delete"]))
):
    logging.info(f"Deleting project: {id}")
    project = project_repository.remove(db=db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully", "project_id": id}
