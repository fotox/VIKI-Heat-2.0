from . import energy
from . import weather
from . import tanks
from . import photovoltaic
from . import heating
from flask import Blueprint

settings_bp = Blueprint("settings", __name__, url_prefix="/api/settings")

# import setting modules
