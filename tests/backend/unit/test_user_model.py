from function.backend.api.auth.user import User


def test_set_and_check_password():
    """Testet das Setzen und Überprüfen eines Passworts"""
    user = User(username="testuser")
    user.set_password("secret123")
    assert user.check_password("secret123") is True
    assert user.check_password("wrongpassword") is False


def test_to_dict_method():
    """Testet die to_dict-Ausgabe"""
    user = User(username="testuser", role="admin")
    result = user.to_dict()
    assert result["username"] == "testuser"
    assert result["role"] == "admin"
    assert "password_hash" not in result
