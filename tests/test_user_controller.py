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


def test_create_user_success(client: TestClient, db: Session):
    """
    Test successful user creation with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    user_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "username": "testuser",
        "password": "TestPassword123!",
        "phone_number": "+1234567890",
        "role_ids": []
    }
    
    response = client.post("/users/", json=user_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["username"] == user_data["username"]
    assert "id" in data


def test_create_user_unauthorized(client: TestClient, db: Session):
    """
    Test user creation without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    user_data = {
        "email": "unauthorizeduser@example.com",
        "full_name": "Unauthorized User",
        "password": "Password123!"
    }
    
    response = client.post("/users/", json=user_data, headers=headers)
    
    assert response.status_code == 403


def test_get_users_success(client: TestClient, db: Session):
    """
    Test successful retrieval of users list with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/users/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # At least admin and basic user should exist


def test_get_users_unauthorized(client: TestClient, db: Session):
    """
    Test users list retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/users/", headers=headers)
    
    assert response.status_code == 403


def test_get_user_by_id_success(client: TestClient, db: Session):
    """
    Test successful retrieval of specific user by ID with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First get list of users to find a valid ID
    users_response = client.get("/users/", headers=headers)
    users = users_response.json()
    user_id = users[0]["id"]
    
    response = client.get(f"/users/{user_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert "email" in data
    assert "full_name" in data


def test_get_user_by_id_not_found(client: TestClient, db: Session):
    """
    Test retrieval of non-existent user should return 404
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/users/99999", headers=headers)
    
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_update_user_success(client: TestClient, db: Session):
    """
    Test successful user update with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create a user to update
    user_data = {
        "email": "updateme@example.com",
        "full_name": "Update Me",
        "password": "Password123!",
        "role_ids": []
    }
    create_response = client.post("/users/", json=user_data, headers=headers)
    user_id = create_response.json()["id"]
    
    # Update the user
    update_data = {
        "full_name": "Updated Name",
        "phone_number": "+9876543210"
    }
    
    response = client.put(f"/users/{user_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["phone_number"] == update_data["phone_number"]


def test_update_user_unauthorized(client: TestClient, db: Session):
    """
    Test user update without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {"full_name": "Unauthorized Update"}
    
    response = client.put("/users/1", json=update_data, headers=headers)
    
    assert response.status_code == 403


def test_delete_user_success(client: TestClient, db: Session):
    """
    Test successful user soft deletion with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create a user to delete
    user_data = {
        "email": "deleteme@example.com",
        "full_name": "Delete Me",
        "password": "Password123!",
        "role_ids": []
    }
    create_response = client.post("/users/", json=user_data, headers=headers)
    user_id = create_response.json()["id"]
    
    # Delete the user
    response = client.delete(f"/users/{user_id}", headers=headers)
    
    assert response.status_code == 200
    # API returns the deleted user object; verify it matches
    assert response.json()["id"] == user_id


def test_delete_user_unauthorized(client: TestClient, db: Session):
    """
    Test user deletion without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete("/users/1", headers=headers)
    
    assert response.status_code == 403 