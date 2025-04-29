from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Text

from extensions import db


class User(db.Model):
    __tablename__ = "users"
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(Text, nullable=False)
    role: str = db.Column(db.String(20), default="user")
    photo = db.Column(db.LargeBinary(length=(5 * 1024 * 1024)), nullable=True)

    def set_password(self, password: str) -> None:
        """Speichert einen Passwort-Hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Vergleicht Klartext-Passwort mit Hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """Gibt Benutzer als dict zurück (ohne Passwort)"""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }
