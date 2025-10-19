from flask import Blueprint

backend_bp = Blueprint("backend", __name__, url_prefix="/")

# import setting modules
if True:
    from . import api
    from . import database
    from . import services
    from . import utils
