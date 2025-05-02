from flask import Blueprint

settings_bp = Blueprint("settings", __name__, url_prefix="/api/settings")

# import setting modules
if True:
    from . import heating
    from . import photovoltaic
    from . import tanks
    from . import weather
    from . import energy
