import pytest
from flask_jwt_extended import create_access_token

from function.backend.app import create_app
from function.backend.extensions import db
from function.backend.models.user import User


@pytest.fixture
def client_and_token():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-jwt-secret"

    client = app.test_client()

    with app.app_context():
        db.create_all()
        user = User(username="admin", role="admin")
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()

        # Token hier korrekt erzeugen
        token = create_access_token(identity={"id": user.id, "role": user.role})

    return client, token


@pytest.fixture
def test_list_devices(client_and_token):
    client, token = client_and_token
    response = client.get(
        "/api/devices/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "devices" in data


@pytest.fixture
def test_toggle_device(client_and_token):
    client, token = client_and_token
    response = client.post("/api/devices/1/toggle",
                           json={
                               "Authorization": f"Bearer {token}"
                           },
                           content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "Switch" in data["msg"]
