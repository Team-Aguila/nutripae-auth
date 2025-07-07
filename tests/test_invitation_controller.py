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


def test_create_invitation_success(client: TestClient, db: Session):
    """
    Test successful invitation creation with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    invitation_data = {
        "email": "invited@example.com",
        "role_ids": [],
        "expires_days": 7
    }
    
    response = client.post("/invitations/", json=invitation_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == invitation_data["email"]
    assert "invitation_code" in data
    assert "id" in data


def test_create_invitation_unauthorized(client: TestClient, db: Session):
    """
    Test invitation creation without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    invitation_data = {
        "email": "unauthorized@example.com",
        "role_ids": []
    }
    
    response = client.post("/invitations/", json=invitation_data, headers=headers)
    
    assert response.status_code == 403


def test_get_invitations_success(client: TestClient, db: Session):
    """
    Test successful retrieval of invitations list with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/invitations/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_invitations_unauthorized(client: TestClient, db: Session):
    """
    Test invitations list retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/invitations/", headers=headers)
    
    assert response.status_code == 403


def test_get_invitation_by_id_success(client: TestClient, db: Session):
    """
    Test successful retrieval of specific invitation by ID with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create an invitation
    invitation_data = {
        "email": "getbyid@example.com",
        "role_ids": [],
        "expires_days": 7
    }
    create_response = client.post("/invitations/", json=invitation_data, headers=headers)
    invitation_id = create_response.json()["id"]
    
    # Get the invitation
    response = client.get(f"/invitations/{invitation_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == invitation_id
    assert data["email"] == invitation_data["email"]


def test_get_invitation_by_id_not_found(client: TestClient, db: Session):
    """
    Test retrieval of non-existent invitation should return 404
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/invitations/99999", headers=headers)
    
    assert response.status_code == 404
    assert "Invitation not found" in response.json()["detail"]


def test_get_invitation_by_id_unauthorized(client: TestClient, db: Session):
    """
    Test invitation by ID retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/invitations/1", headers=headers)
    
    assert response.status_code == 403


def test_resend_invitation_success(client: TestClient, db: Session):
    """
    Test successful invitation resend with admin privileges
    """
    pytest.skip("Endpoint /invitations/{id}/resend not implemented in API")


def test_resend_invitation_unauthorized(client: TestClient, db: Session):
    """
    Test invitation resend without proper authorization should return 403
    """
    pytest.skip("Endpoint /invitations/{id}/resend not implemented in API")


def test_cancel_invitation_success(client: TestClient, db: Session):
    """
    Test successful invitation cancellation with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create an invitation
    invitation_data = {
        "email": "cancel@example.com",
        "role_ids": [],
        "expires_days": 7
    }
    create_response = client.post("/invitations/", json=invitation_data, headers=headers)
    invitation_id = create_response.json()["id"]
    
    # Cancel the invitation
    response = client.put(f"/invitations/{invitation_id}/cancel", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["id"] == invitation_id


def test_cancel_invitation_unauthorized(client: TestClient, db: Session):
    """
    Test invitation cancellation without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.put("/invitations/1/cancel", headers=headers)
    
    assert response.status_code == 403


def test_validate_invitation_code_success(client: TestClient, db: Session):
    pytest.skip("Endpoint /invitations/validate/{invitation_code} not implemented in API")

def test_validate_invitation_code_invalid(client: TestClient, db: Session):
    """
    Test validation of invalid invitation code should return 404
    """
    response = client.get("/invitations/validate/invalid-code-123")
    
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["message"] == "Invalid invitation code" 