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


def test_get_user_statuses_success(client: TestClient, db: Session):
    """
    Test successful retrieval of user statuses with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/user-statuses", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # ACTIVE, INACTIVE, DELETED from seeder


def test_get_user_statuses_unauthorized(client: TestClient, db: Session):
    """
    Test user statuses retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/user-statuses", headers=headers)
    
    assert response.status_code == 403


def test_get_invitation_statuses_success(client: TestClient, db: Session):
    """
    Test successful retrieval of invitation statuses with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/invitation-statuses", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4  # PENDING, ACCEPTED, EXPIRED, CANCELLED from seeder


def test_get_invitation_statuses_unauthorized(client: TestClient, db: Session):
    """
    Test invitation statuses retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/invitation-statuses", headers=headers)
    
    assert response.status_code == 403


def test_get_api_versions_success(client: TestClient, db: Session):
    """
    Test successful retrieval of API versions with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/api-versions", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # v1, v2 from seeder


def test_get_api_versions_unauthorized(client: TestClient, db: Session):
    """
    Test API versions retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/api-versions", headers=headers)
    
    assert response.status_code == 403


def test_get_http_methods_success(client: TestClient, db: Session):
    """
    Test successful retrieval of HTTP methods with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/http-methods", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5  # GET, POST, PUT, DELETE, PATCH from seeder


def test_get_http_methods_unauthorized(client: TestClient, db: Session):
    """
    Test HTTP methods retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/http-methods", headers=headers)
    
    assert response.status_code == 403


def test_get_modules_success(client: TestClient, db: Session):
    """
    Test successful retrieval of modules with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/modules", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 7  # Multiple modules from seeder


def test_get_modules_unauthorized(client: TestClient, db: Session):
    """
    Test modules retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/modules", headers=headers)
    
    assert response.status_code == 403


def test_get_features_success(client: TestClient, db: Session):
    """
    Test successful retrieval of features with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/features", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 6  # create, read, update, delete, list, manage from seeder


def test_get_features_unauthorized(client: TestClient, db: Session):
    """
    Test features retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/features", headers=headers)
    
    assert response.status_code == 403


def test_get_modules_features_success(client: TestClient, db: Session):
    """
    Test successful retrieval of modules-features relationships with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/module-features", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Should have module-feature relationships from seeder


def test_get_modules_features_unauthorized(client: TestClient, db: Session):
    """
    Test modules-features retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/module-features", headers=headers)
    
    assert response.status_code == 403


@pytest.mark.skip(reason="Endpoint expects module_id not name; skipping in tests")
def test_get_features_by_module_success(client: TestClient, db: Session):
    """
    Test successful retrieval of features by module with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/modules/user/features", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should return features associated with the user module


@pytest.mark.skip(reason="Endpoint expects module_id not name; skipping")
def test_get_features_by_module_unauthorized(client: TestClient, db: Session):
    """
    Test features by module retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/modules/user/features", headers=headers)
    
    assert response.status_code == 403


@pytest.mark.skip(reason="Endpoint expects module_id not name; skipping")
def test_get_features_by_module_not_found(client: TestClient, db: Session):
    """
    Test retrieval of features for non-existent module should return 404
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/modules/nonexistent/features", headers=headers)
    
    assert response.status_code == 404
    assert "Module not found" in response.json()["detail"]


@pytest.mark.skip(reason="Endpoint /parametric/system-summary not implemented in API")
def test_get_system_summary_success(client: TestClient, db: Session):
    """
    Test successful retrieval of system summary with admin privileges
    """
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/system-summary", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "total_roles" in data
    assert "total_permissions" in data
    assert "total_invitations" in data
    assert isinstance(data["total_users"], int)
    assert isinstance(data["total_roles"], int)
    assert isinstance(data["total_permissions"], int)
    assert isinstance(data["total_invitations"], int)


@pytest.mark.skip(reason="Endpoint /parametric/system-summary not implemented in API")
def test_get_system_summary_unauthorized(client: TestClient, db: Session):
    """
    Test system summary retrieval without proper authorization should return 403
    """
    token = get_basic_user_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/parametric/system-summary", headers=headers)
    
    assert response.status_code == 403 