import os
import io

from flask import Blueprint, request, jsonify, send_file, Response
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    jwt_required,
    get_jwt_identity,
)
from config import Config
from extensions import db
from database.users import User

from utils.logging_service import LoggingService

auth_bp = Blueprint("auth", __name__)

FALLBACK_PATH = os.path.join(os.path.dirname(__file__), "static", "blank_user.png")

logging = LoggingService()


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates a user and returns a JWT token and user data.

    Expects:
        JSON body with 'username' and 'password'.

    Returns:
        200 OK with JWT token and user info if credentials are valid.
        401 Unauthorized if login fails.
    """
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    if not user or not user.check_password(data.get("password")):
        logging.info("Invalid username or password")
        return jsonify(msg="Invalid username or password"), 401

    additional: dict = {"role": user.role}
    token: str = create_access_token(
        identity=str(user.id),
        additional_claims=additional
    )

    resp: Response = jsonify(user=user.to_dict())
    set_access_cookies(resp, token)
    logging.info("Login successful")
    return resp, 200


@auth_bp.route("/profile/photo", methods=["GET"])
@jwt_required(optional=True)
def profile_photo():
    """
    Returns the profile photo of the currently authenticated user. If there is no login **or** no photo is saved,
    a placeholder image (`blank_user.png`) is returned.

    Returns:
      200 OK
        • image/jpeg – if a user photo is available
        • image/png  – if not registered or photo is missing
    """
    def _fallback():
        return send_file(
            FALLBACK_PATH,
            mimetype="image/png",
            download_name="avatar.png",
        )

    identity = get_jwt_identity()
    if not identity:
        return _fallback()

    user = User.query.get(identity)
    if not user or not user.photo:
        return _fallback()

    return send_file(
        io.BytesIO(user.photo),
        mimetype="image/jpeg",
        download_name="avatar.jpg",
    )


@auth_bp.route("/register", methods=["POST"])
@jwt_required()
def register() -> tuple:
    """
    Registers a new user (admin-only access).

    Expects:
        JSON body with at least 'username' and 'password'.
        Optional 'role' (defaults to "user").

    Returns:
        201 Created on success.
        403 Forbidden if requester is not admin.
        409 Conflict if username already exists.
    """
    """Nur Admins dürfen neue Benutzer anlegen"""
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        logging.info("Only admins can register new users.")
        return jsonify(msg="Only admins can register new users."), 403

    data = request.get_json()
    if User.query.filter_by(username=data.get("username")).first():
        logging.info("Username already exists.")
        return jsonify(msg="Username already exists."), 409

    user: User = User(username=data["username"], role=data.get("role", "user"))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    logging.info("New user registered.")
    return jsonify(msg="New user registered."), 201


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password() -> tuple:
    """
    Resets a user's password using a master key.

    Expects:
        JSON body with 'username', 'new_password', and 'master_key'.

    Returns:
        200 OK if password was successfully reset.
        403 Forbidden if master key is invalid.
        404 Not Found if the user does not exist.
    """
    data = request.get_json()
    if data.get("master_key") != Config.MASTER_RESET_KEY:
        logging.info("Invalid master key.")
        return jsonify(msg="Invalid master key."), 403

    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        logging.info("User not found.")
        return jsonify(msg="User not found."), 404

    user.set_password(data["new_password"])
    db.session.commit()
    logging.info("Password reset successful.")
    return jsonify(msg="Password reset successful."), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required
def profile():
    """
    Returns the profile data of the authenticated user.

    Returns:
        200 OK with user's public profile information.
        401 Unauthorized if token is invalid or user does not exist.
    """
    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({"msg": "Authentication required."}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found."}), 401

    return jsonify(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        role=user.role,
        email=user.email,
        phone=user.phone
    ), 200


@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """
    Updates the authenticated user's profile data.

    Accepts multipart/form-data with optional fields:
        - firstname (str)
        - lastname (str)
        - username (str)
        - email (str)
        - phone (str)
        - password (str)
        - photo (file, image/jpeg or image/png, max 5MB)

    Returns:
        200 OK if update succeeds.
        413 Payload Too Large if image exceeds size limit.
        415 Unsupported Media Type if image format is invalid.
    """
    user = User.query.get(get_jwt_identity())
    form = request.form
    if "firstname" in form:
        user.firstname = form["firstname"]
    if "lastname" in form:
        user.lastname = form["lastname"]
    if "username" in form:
        user.username = form["username"]
    if "password" in form and form["password"]:
        user.set_password(form["password"])
    if "email" in form:
        user.email = form["email"]
    if "phone" in form:
        user.phone = form["phone"]
    if "photo" in request.files:
        file = request.files["photo"]
        if file and file.mimetype in ("image/png", "image/jpeg"):
            data = file.read()
            if len(data) <= 5 * 1024 * 1024:
                user.photo = data
            else:
                logging.info("Image too large.")
                return jsonify(msg="Image too large."), 413
        else:
            logging.info("Invalid file type.")
            return jsonify(msg="Invalid file type."), 415

    db.session.commit()
    logging.info(f"Profile '{user.username}' update successful.")
    return jsonify(msg=f"Profile '{user.username}' update successful."), 200
