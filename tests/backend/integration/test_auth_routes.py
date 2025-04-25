import pytest

from backend.app import create_app
from backend.extensions import db
from backend.models.user import User


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        user = User(username="admin", role="admin")
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()
    return app.test_client()


def test_login_success(client):
    res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    assert "token" in res.get_json()


def test_login_fail(client):
    res = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert res.status_code == 401
