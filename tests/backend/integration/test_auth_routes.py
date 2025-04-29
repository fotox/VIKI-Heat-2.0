import pytest
from flask_jwt_extended import create_access_token

from backend.services.user import User
from function.backend.app import create_app
from function.backend.extensions import db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


@pytest.fixture
def test_login_success(client):
    """Test gültigen Login"""
    response = client.post("/api/auth/login",
                           json={
                               "username": "admin",
                               "password": "admin123"
                           },
                           content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert data["user"]["username"] == "admin"


@pytest.fixture
def test_login_fail(client):
    """Test fehlgeschlagener Login"""
    response = client.post("/api/auth/login",
                           json={
                               "username": "admin",
                               "password": "wrongpassword"
                           },
                           content_type="application/json")
    assert response.status_code == 401


def test_register_without_admin():
    """Registration ohne Admin-Rechte → 403"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-jwt-secret"

    with app.app_context():
        db.create_all()
        user = User(username="user_test_register", role="user")
        user.set_password("secret")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity={"id": user.id, "role": user.role})

    client = app.test_client()
    response = client.post(
        "/api/auth/register",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "anotheruser", "password": "pw"}
    )
    assert response.status_code == 422


def test_reset_password_invalid_master_key():
    """Reset mit falschem Master-Key → 403"""
    client = create_app().test_client()
    response = client.post("/api/auth/reset-password", json={
        "username": "admin",
        "new_password": "newpw",
        "master_key": "wrongkey"
    })
    assert response.status_code == 403
