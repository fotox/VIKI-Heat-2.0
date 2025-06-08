from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from database.settings import WeatherSetting
from . import settings_bp


@settings_bp.route("/weather", methods=["GET"])
def list_weather_modules():
    """
    GET /api/settings/weather
    Returns a list of weather modules
    """
    modules = WeatherSetting.query.order_by(WeatherSetting.id).all()
    return jsonify(modules=[m.to_dict() for m in modules]), 200


@settings_bp.route("/weather", methods=["POST"])
@jwt_required()
def create_weather_module():
    """
    POST /api/settings/weather
    Create a new weather element. Json required:
      - description (string)
      - manufacturer (ManufacturerSettings)
      - location (LocationSettings)
      - ip (string)
      - api_key (string)
    """
    data = request.get_json() or {}
    required = ["description", "manufacturer", "location", "ip", "api_key"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Missing fields: {', '.join(missing)}"), 422

    module = WeatherSetting(
        description=data["description"],
        manufacturer=data["manufacturer"],
        location=data["location"],
        ip=data["ip"],
        api_key=data["api_key"]
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/weather/<int:module_id>", methods=["PUT"])
@jwt_required()
def update_weather_module(module_id: int):
    """
    PUT /api/settings/weather/<module_id>
    Update a new weather element. Json required:
      - description (string)
      - manufacturer (ManufacturerSettings)
      - location (LocationSettings)
      - ip (string)
      - api_key (string)
    """
    module = WeatherSetting.query.get_or_404(module_id)
    data = request.get_json() or {}

    for key in ("description", "manufacturer", "location", "ip", "api_key"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200


@settings_bp.route("/weather/<int:module_id>", methods=["DELETE"])
@jwt_required()
def delete_weather_module(module_id):
    mod = WeatherSetting.query.get_or_404(module_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204
