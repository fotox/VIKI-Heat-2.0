import pytest

from function.backend.extensions import db
from function.backend.models.user import User
from function.backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SECRET_KEY"] = "test-secret"
    app.config["JWT_SECRET_KEY"] = "test-jwt-secret"

    with app.app_context():
        db.create_all()
        user = User(username="admin", role="admin")
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()

    return app.test_client()
