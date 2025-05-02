from flask import Blueprint

utils_bp = Blueprint("utils", __name__, url_prefix="/utils")

# import setting modules
if True:
    from . import logging_service
