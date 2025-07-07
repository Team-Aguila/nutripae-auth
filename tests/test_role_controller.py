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


def test_create_role_success(client: TestClient, db: Session):
    """
    Test successful role creation with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    role_data = {
        "name": "Test Role",
        "description": "Test role description",
        "permission_ids": []
    }
    
    response = client.post("/roles/", json=role_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == role_data["name"]
    assert data["description"] == role_data["description"]
    assert "id" in data


def test_create_role_unauthorized(client: TestClient, db: Session):
    """
    Test role creation without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    role_data = {
        "name": "Unauthorized Role",
        "description": "This should not be created"
    }
    
    response = client.post("/roles/", json=role_data, headers=headers)
    
    assert response.status_code == 403


def test_get_roles_success(client: TestClient, db: Session):
    """
    Test successful retrieval of roles list with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/roles/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # At least Super Admin, Project Admin, and Basic User should exist


def test_get_roles_unauthorized(client: TestClient, db: Session):
    """
    Test roles list retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/roles/", headers=headers)
    
    assert response.status_code == 403


def test_get_role_by_id_success(client: TestClient, db: Session):
    """
    Test successful retrieval of specific role by ID with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First get list of roles to find a valid ID
    roles_response = client.get("/roles/", headers=headers)
    roles = roles_response.json()
    role_id = roles[0]["id"]
    
    response = client.get(f"/roles/{role_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == role_id
    assert "name" in data
    assert "description" in data


def test_get_role_by_id_not_found(client: TestClient, db: Session):
    """
    Test retrieval of non-existent role should return 404
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/roles/99999", headers=headers)
    
    assert response.status_code == 404
    assert "Role not found" in response.json()["detail"]


def test_update_role_success(client: TestClient, db: Session):
    """
    Test successful role update with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create a role to update
    role_data = {
        "name": "Update Me Role",
        "description": "Original description",
        "permission_ids": []
    }
    create_response = client.post("/roles/", json=role_data, headers=headers)
    role_id = create_response.json()["id"]
    
    # Update the role
    update_data = {
        "name": "Updated Role Name",
        "description": "Updated description"
    }
    
    response = client.put(f"/roles/{role_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]


def test_update_role_unauthorized(client: TestClient, db: Session):
    """
    Test role update without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {"name": "Unauthorized Update"}
    
    response = client.put("/roles/1", json=update_data, headers=headers)
    
    assert response.status_code == 403


def test_delete_role_success(client: TestClient, db: Session):
    """
    Test successful role deletion with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create a role to delete
    role_data = {
        "name": "Delete Me Role",
        "description": "This role will be deleted",
        "permission_ids": []
    }
    create_response = client.post("/roles/", json=role_data, headers=headers)
    role_id = create_response.json()["id"]
    
    # Delete the role
    response = client.delete(f"/roles/{role_id}", headers=headers)
    
    assert response.status_code == 200
    # API returns deleted role object; verify id matches
    assert response.json()["id"] == role_id


def test_delete_role_unauthorized(client: TestClient, db: Session):
    """
    Test role deletion without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete("/roles/1", headers=headers)
    
    assert response.status_code == 403


def test_get_role_users_success(client: TestClient, db: Session):
    """
    Test successful retrieval of users assigned to a role with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get list of roles to find one with users
    roles_response = client.get("/roles/", headers=headers)
    roles = roles_response.json()
    # Find the "Super Admin" role which should have users
    role_id = None
    for role in roles:
        if role["name"] == "Super Admin":
            role_id = role["id"]
            break
    
    if role_id:
        response = client.get(f"/roles/{role_id}/users", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


def test_get_role_users_unauthorized(client: TestClient, db: Session):
    """
    Test role users retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/roles/1/users", headers=headers)
    
    assert response.status_code == 403 