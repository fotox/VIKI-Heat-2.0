from . import others
from . import weather
from . import watertank
from . import photovoltaic
from flask import Blueprint

settings_bp = Blueprint("settings", __name__, url_prefix="/api/settings")

# import setting modules
