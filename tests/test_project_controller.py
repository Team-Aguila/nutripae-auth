import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from core.config import settings


def get_admin_token(client: TestClient) -> str:
    """Helper function to get admin token for authentication"""
    login_data = {"email": settings.ADMIN_EMAIL, "password": settings.ADMIN_PASSWORD}
    response = client.post("/auth/login", json=login_data)
    return response.json()["access_token"]


def get_basic_user_token(client: TestClient) -> str:
    """Helper function to get basic user token for authentication"""
    login_data = {"email": "user@example.com", "password": "Password123!"}
    response = client.post("/auth/login", json=login_data)
    return response.json()["access_token"]


def test_create_project_success(client: TestClient, db: Session):
    """
    Test successful project creation with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    project_data = {
        "name": "Test Project"
    }
    
    response = client.post("/projects/", json=project_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == project_data["name"]
    assert "id" in data


def test_create_project_unauthorized(client: TestClient, db: Session):
    """
    Test project creation without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    project_data = {
        "name": "Unauthorized Project"
    }
    
    response = client.post("/projects/", json=project_data, headers=headers)
    
    assert response.status_code == 403


def test_get_projects_success(client: TestClient, db: Session):
    """
    Test successful retrieval of projects list with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/projects/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least "Default Project" should exist


def test_get_projects_basic_user_success(client: TestClient, db: Session):
    """
    Test projects list retrieval with basic user - should succeed as basic user has project:read permission
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/projects/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_project_by_id_success(client: TestClient, db: Session):
    """
    Test successful retrieval of specific project by ID with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First get list of projects to find a valid ID
    projects_response = client.get("/projects/", headers=headers)
    projects = projects_response.json()
    project_id = projects[0]["id"]
    
    response = client.get(f"/projects/{project_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert "name" in data


def test_get_project_by_id_not_found(client: TestClient, db: Session):
    """
    Test retrieval of non-existent project should return 404
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/projects/99999", headers=headers)
    
    assert response.status_code == 404
    assert "Project not found" in response.json()["detail"]


def test_get_project_by_id_basic_user_success(client: TestClient, db: Session):
    """
    Test project by ID retrieval with basic user - should succeed as basic user has project:read permission
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First get list of projects to find a valid ID
    projects_response = client.get("/projects/", headers=headers)
    projects = projects_response.json()
    
    if projects:  # Only test if there are projects
        project_id = projects[0]["id"]
        response = client.get(f"/projects/{project_id}", headers=headers)
        assert response.status_code == 200


def test_update_project_success(client: TestClient, db: Session):
    """
    Test successful project update with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create a project to update
    project_data = {
        "name": "Update Me Project"
    }
    create_response = client.post("/projects/", json=project_data, headers=headers)
    project_id = create_response.json()["id"]
    
    # Update the project
    update_data = {
        "name": "Updated Project Name"
    }
    response = client.put(f"/projects/{project_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]


def test_update_project_unauthorized(client: TestClient, db: Session):
    """
    Test project update without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "name": "Unauthorized Update"
    }
    
    response = client.put("/projects/1", json=update_data, headers=headers)
    
    assert response.status_code == 403


def test_delete_project_success(client: TestClient, db: Session):
    """
    Test successful project deletion with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create a project to delete
    project_data = {
        "name": "Delete Me Project"
    }
    create_response = client.post("/projects/", json=project_data, headers=headers)
    project_id = create_response.json()["id"]
    
    # Delete the project
    response = client.delete(f"/projects/{project_id}", headers=headers)
    
    assert response.status_code == 200
    assert "Project deleted successfully" in response.json()["message"]


def test_delete_project_unauthorized(client: TestClient, db: Session):
    """
    Test project deletion without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete("/projects/1", headers=headers)
    
    assert response.status_code == 403 