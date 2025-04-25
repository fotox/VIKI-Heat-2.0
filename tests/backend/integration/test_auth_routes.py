import pytest

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


def test_login_success(client):
    """Test erfolgreicher Login"""
    response = client.post("/api/auth/login",
                           json={
                               "username": "admin",
                               "password": "admin123"
                           },
                           content_type="application/json")  # <-- wichtig!
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert data["user"]["username"] == "admin"


def test_login_fail(client):
    """Test fehlgeschlagener Login"""
    response = client.post("/api/auth/login",
                           json={
                               "username": "admin",
                               "password": "wrongpassword"
                           },
                           content_type="application/json")  # <-- wichtig!
    assert response.status_code == 401
