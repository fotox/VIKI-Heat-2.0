from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey

from extensions import db


class Role(db.Model):
    __tablename__ = "roles"
    id: int = db.Column(db.INTEGER, primary_key=True)
    role_name: str = db.Column(db.VARCHAR(256), unique=True, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "role_name": self.role_name,
        }


class User(db.Model):
    __tablename__ = "users"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    username: db.Mapped[str] = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    firstname: db.Mapped[str] = db.Column(db.VARCHAR(64), unique=True, nullable=True)
    lastname: db.Mapped[str] = db.Column(db.VARCHAR(64), unique=True, nullable=True)
    password_hash: db.Mapped[str] = db.Column(db.TEXT, nullable=False)
    role: db.Mapped["Role"] = db.mapped_column(ForeignKey(Role.role_name), nullable=False)
    photo: db.Mapped[bytes] = db.Column(db.LargeBinary(length=(5 * 1024 * 1024)), nullable=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "password_hash": self.password_hash,
            "role": self.role,
        }
