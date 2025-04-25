import pytest
from function.backend.app import create_app
from function.backend.extensions import db
from function.backend.models.user import User
from flask_jwt_extended import create_access_token


@pytest.fixture
def client_with_auth():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-jwt-secret"

    with app.app_context():
        db.create_all()
        admin = User(username="admin", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

    client = app.test_client()

    with app.app_context():
        token = create_access_token(identity={"id": admin.id, "role": admin.role})

    return client, token


def test_list_devices(client_with_auth):
    """Testet ob die Geräte-Liste erfolgreich abrufbar ist"""
    client, token = client_with_auth
    response = client.get(
        "/api/devices/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "devices" in data
    assert isinstance(data["devices"], list)


def test_toggle_device(client_with_auth):
    """Testet das Umschalten eines Gerätes"""
    client, token = client_with_auth
    response = client.post(
        "/api/devices/1/toggle",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Switch" in response.get_json()["msg"]
