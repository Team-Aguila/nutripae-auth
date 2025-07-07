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


def test_check_authorization_success(client: TestClient, db: Session):
    """
    Test successful authorization check with valid token and permissions
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    auth_request = {
        "endpoint": "/users/",
        "method": "GET",
        "required_permissions": ["user:list"]
    }
    
    response = client.post("/authorization/check-authorization", json=auth_request, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["authorized"] is True


def test_check_authorization_insufficient_permissions(client: TestClient, db: Session):
    """
    Test authorization check with insufficient permissions - returns 200 with authorized=false
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    auth_request = {
        "endpoint": "/users/",
        "method": "POST",
        "required_permissions": ["user:create"]  # Basic user doesn't have this permission
    }
    
    response = client.post("/authorization/check-authorization", json=auth_request, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["authorized"] == False
    assert "user:create" in data["missing_permissions"]


def test_check_authorization_no_token(client: TestClient, db: Session):
    """
    Test authorization check without token should return 403
    """
    auth_request = {
        "endpoint": "/users/",
        "method": "GET",
        "required_permissions": ["user:list"]
    }
    
    response = client.post("/authorization/check-authorization", json=auth_request)
    
    assert response.status_code == 403


def test_check_authorization_invalid_token(client: TestClient, db: Session):
    """
    Test authorization check with invalid token should return 401
    """
    headers = {"Authorization": "Bearer invalid_token_123"}
    
    auth_request = {
        "endpoint": "/users/",
        "method": "GET",
        "required_permissions": ["user:list"]
    }
    
    response = client.post("/authorization/check-authorization", json=auth_request, headers=headers)
    
    assert response.status_code == 401


def test_get_user_permissions_success(client: TestClient, db: Session):
    """
    Test successful retrieval of user permissions with valid token
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/authorization/user-permissions", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "permissions" in data
    assert isinstance(data["permissions"], list)
    assert len(data["permissions"]) > 0  # Admin should have permissions


def test_get_user_permissions_no_token(client: TestClient, db: Session):
    """
    Test user permissions retrieval without token should return 403
    """
    response = client.get("/authorization/user-permissions")
    
    assert response.status_code == 403


def test_get_user_permissions_invalid_token(client: TestClient, db: Session):
    """
    Test user permissions retrieval with invalid token should return 401
    """
    headers = {"Authorization": "Bearer invalid_token_123"}
    
    response = client.get("/authorization/user-permissions", headers=headers)
    
    assert response.status_code == 401


@pytest.mark.skip(reason="Endpoint /authorization/user-info not implemented in API")
def test_get_user_info_success(client: TestClient, db: Session):
    """
    Test successful retrieval of user info with valid token
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/authorization/user-info", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "email" in data
    assert "role" in data
    assert "permissions" in data
    assert data["email"] == "admin@example.com"


@pytest.mark.skip(reason="Endpoint /authorization/user-info not implemented in API")
def test_get_user_info_no_token(client: TestClient, db: Session):
    """
    Test user info retrieval without token should return 401
    """
    response = client.get("/authorization/user-info")
    
    assert response.status_code == 401


@pytest.mark.skip(reason="Endpoint /authorization/user-info not implemented in API")
def test_get_user_info_invalid_token(client: TestClient, db: Session):
    """
    Test user info retrieval with invalid token should return 401
    """
    headers = {"Authorization": "Bearer invalid_token_123"}
    
    response = client.get("/authorization/user-info", headers=headers)
    
    assert response.status_code == 401


@pytest.mark.skip(reason="Endpoint /authorization/validate-permission not implemented in API")
def test_validate_specific_permission_success(client: TestClient, db: Session):
    """
    Test successful validation of specific permission with valid token
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/authorization/validate-permission/user:list", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["has_permission"] == True
    assert data["permission"] == "user:list"


@pytest.mark.skip(reason="Endpoint /authorization/validate-permission not implemented in API")
def test_validate_specific_permission_insufficient(client: TestClient, db: Session):
    """
    Test validation of specific permission with insufficient privileges
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/authorization/validate-permission/user:create", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["has_permission"] == False
    assert data["permission"] == "user:create"


@pytest.mark.skip(reason="Endpoint /authorization/validate-permission not implemented in API")
def test_validate_specific_permission_no_token(client: TestClient, db: Session):
    """
    Test specific permission validation without token should return 401
    """
    response = client.get("/authorization/validate-permission/user:list")
    
    assert response.status_code == 401


@pytest.mark.skip(reason="Endpoint /authorization/validate-permission not implemented in API")
def test_validate_specific_permission_invalid_token(client: TestClient, db: Session):
    """
    Test specific permission validation with invalid token should return 401
    """
    headers = {"Authorization": "Bearer invalid_token_123"}
    
    response = client.get("/authorization/validate-permission/user:list", headers=headers)
    
    assert response.status_code == 401 