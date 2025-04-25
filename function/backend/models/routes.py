"""
Routen zur Authentifizierung (Login, Registrierung, Passwort-Reset).
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from function.backend.config import Config
from function.backend.extensions import db
from function.backend.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login() -> tuple:
    """Login per Username & Passwort"""
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()

    if user and user.check_password(data.get("password")):
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify(token=token, user=user.to_dict()), 200
    return jsonify(msg="Ungültige Anmeldedaten"), 401


@auth_bp.route("/register", methods=["POST"])
@jwt_required()
def register() -> tuple:
    """Nur Admins dürfen neue Benutzer anlegen"""
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify(msg="Nur Admins dürfen neue Benutzer erstellen"), 403

    data = request.get_json()
    if User.query.filter_by(username=data.get("username")).first():
        return jsonify(msg="Benutzername existiert bereits"), 409

    user = User(username=data["username"], role=data.get("role", "user"))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="Benutzer erfolgreich angelegt"), 201


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password() -> tuple:
    """Passwort zurücksetzen per Master-Key"""
    data = request.get_json()
    if data.get("master_key") != Config.MASTER_RESET_KEY:
        return jsonify(msg="Ungültiger Master-Key"), 403

    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify(msg="Benutzer nicht gefunden"), 404

    user.set_password(data["new_password"])
    db.session.commit()
    return jsonify(msg="Passwort erfolgreich zurückgesetzt"), 200
