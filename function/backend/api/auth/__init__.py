from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# import auth modules
if True:
    from . import routes
