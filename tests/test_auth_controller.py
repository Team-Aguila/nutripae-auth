import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from core.config import settings




def test_register_success(client: TestClient, db: Session):
    """
    Test successful user registration
    """
    user_data = {
        "email": "newuser@example.com",
        "full_name": "New User",
        "username": "newuser",
        "password": "NewPassword123!",
        "phone_number": "+1234567890"
    }
    
    response = client.post("/auth/register", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["username"] == user_data["username"]
    assert "id" in data


def test_register_duplicate_email(client: TestClient, db: Session):
    """
    Test registration with duplicate email should return 400
    """
    user_data = {
        "email": "admin@example.com",  # This email already exists
        "full_name": "Another Admin",
        "password": "Password123!"
    }
    
    response = client.post("/auth/register", json=user_data)
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_change_password_success(client: TestClient, db: Session):
    """
    Test successful password change with valid authentication
    """
    # First login to get token
    login_data = {"email": "user@example.com", "password": "Password123!"}
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    # Change password
    password_data = {
        "old_password": "Password123!",
        "new_password": "NewPassword456!"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/auth/change-password", json=password_data, headers=headers)
    
    assert response.status_code == 200
    assert "Password changed successfully" in response.json()["message"]


def test_change_password_wrong_old_password(client: TestClient, db: Session):
    """
    Test password change with incorrect old password should return 400
    """
    # First login to get token
    login_data = {"email": "user@example.com", "password": "Password123!"}
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    # Try to change password with wrong old password
    password_data = {
        "old_password": "WrongOldPassword",
        "new_password": "NewPassword456!"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/auth/change-password", json=password_data, headers=headers)
    
    assert response.status_code == 400
    assert "Incorrect old password" in response.json()["detail"]


def test_forgot_password_success(client: TestClient, db: Session):
    """
    Test forgot password endpoint (always returns success for security)
    """
    response = client.post("/auth/forgot-password", params={"email": "admin@example.com"})
    
    assert response.status_code == 200
    assert "If the email exists, you will receive password reset instructions" in response.json()["message"]


def test_forgot_password_nonexistent_email(client: TestClient, db: Session):
    """
    Test forgot password with non-existent email (should still return success for security)
    """
    response = client.post("/auth/forgot-password", params={"email": "nonexistent@example.com"})
    
    assert response.status_code == 200
    assert "If the email exists, you will receive password reset instructions" in response.json()["message"] 