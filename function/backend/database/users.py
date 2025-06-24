from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey

from extensions import db


class Role(db.Model):
    """
    Represents a user role within the system.

    Used to assign permissions or access levels to users.

    Attributes:
        id (int): Unique identifier of the role.
        role_name (str): Name of the role (must be unique, e.g., "admin", "user").
    """
    __tablename__ = "roles"
    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    role_name: db.Mapped[str] = db.Column(db.VARCHAR(256), unique=True, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "role_name": self.role_name,
        }


class User(db.Model):
    """
    Represents a system user with credentials and associated role.

    Attributes:
        id (int): Unique identifier of the user.
        username (str): Unique login name of the user.
        firstname (str): Optional first name of the user.
        lastname (str): Optional last name of the user.
        email (str): Optional email address.
        phone (str): Optional phone number.
        password_hash (str): Hashed password for authentication.
        role (Role): Foreign key reference to the user's role.
        photo (bytes): Optional user photo (max 5MB).
    """
    __tablename__ = "users"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    username: db.Mapped[str] = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    firstname: db.Mapped[str] = db.Column(db.VARCHAR(64), unique=True, nullable=True)
    lastname: db.Mapped[str] = db.Column(db.VARCHAR(64), unique=True, nullable=True)
    email: db.Mapped[str] = db.Column(db.VARCHAR(64), nullable=True)
    phone: db.Mapped[str] = db.Column(db.VARCHAR(64), nullable=True)
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
            "email": self.email,
            "phone": self.phone,
            "password_hash": self.password_hash,
            "role": self.role,
        }
