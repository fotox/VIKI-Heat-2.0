"""
Routen zur Authentifizierung (Login, Registrierung, Passwort-Reset).
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies

from config import Config
from extensions import db
from api.auth.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    if not user or not user.check_password(data.get("password")):
        return jsonify(msg="Ungültige Anmeldedaten"), 401

    additional = {"role": user.role}
    token = create_access_token(
        identity=str(user.id),
        additional_claims=additional
    )

    resp = jsonify(user=user.to_dict())
    set_access_cookies(resp, token)
    return resp, 200


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


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """Gibt Username und Rolle des eingeloggten Nutzers zurück"""
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])
    return jsonify(username=user.username, role=user.role), 200
