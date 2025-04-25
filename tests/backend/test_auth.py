"""
Testet Login-Endpoint der Authentifizierung.
"""

import pytest

from function.backend.app import create_app
from function.backend.extensions import db
from function.backend.models.user import User


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        # Testuser
        user = User(username="testuser")
        user.set_password("secret")
        db.session.add(user)
        db.session.commit()
    return app.test_client()


def test_login_success(client):
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "secret"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_login_fail(client):
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "wrong"
    })
    assert response.status_code == 401
