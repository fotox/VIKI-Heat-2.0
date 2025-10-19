from flask import Blueprint

database_bp = Blueprint("database", __name__, url_prefix="/database")

# import database modules
if True:
    from . import init_db
    from . import settings
    from . import users
