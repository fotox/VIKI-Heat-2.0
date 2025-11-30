from flask import Blueprint

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")

# import dashboard modules
if True:
    from . import routes
    from . import modules
