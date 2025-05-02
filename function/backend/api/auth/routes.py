from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    jwt_required,
    get_jwt_identity,
)

from config import Config
from extensions import db
from database.users import User
import io

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


@auth_bp.route("/profile/photo", methods=["GET"])
@jwt_required()
def profile_photo():
    """Gibt das Avatar-Bild als image/jpeg oder image/png zurück."""
    user = User.query.get(get_jwt_identity())
    if not user or not user.photo:
        return send_file(
            io.BytesIO(open("function/backend/static/default-avatar.png", "rb").read()),
            mimetype="image/png"
        )
    return send_file(
        io.BytesIO(user.photo),
        mimetype="image/jpeg"
    )


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
    user_id = get_jwt_identity()      # gibt z.B. 1 zurück
    user = User.query.get(user_id)
    return jsonify(username=user.username, role=user.role), 200


@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """
    Aktualisiert Username, evtl. Passwort (optional) und Photo.
    Erwartet multipart/form-data mit Feldern:
    - username (string)
    - password (optional, string)
    - photo (optional, file)
    """
    user = User.query.get(get_jwt_identity())   # TODO: Erweitern auf alle Benutzerprofilinformationen
    form = request.form
    if "username" in form:
        user.username = form["username"]
    if "password" in form and form["password"]:
        user.set_password(form["password"])
    if "photo" in request.files:
        file = request.files["photo"]
        if file and file.mimetype in ("image/png", "image/jpeg"):
            data = file.read()
            if len(data) <= 5 * 1024 * 1024:
                user.photo = data
            else:
                return jsonify(msg="Datei zu groß"), 413
        else:
            return jsonify(msg="Ungültiges Dateiformat"), 415

    db.session.commit()
    return jsonify(msg="Profil aktualisiert"), 200
