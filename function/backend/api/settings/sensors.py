from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from database.settings import SensorSetting, TankSetting
from . import settings_bp


@settings_bp.route("/sensor", methods=["GET"])
def list_sensor_modules():
    """
    GET /api/settings/sensor
    Return list of sensor modules.
    """
    modules = SensorSetting.query.order_by(SensorSetting.id).all()
    return jsonify(modules=[m.to_dict() for m in modules]), 200


@settings_bp.route("/sensor", methods=["POST"])
@jwt_required()
def create_sensor_module():
    """
    POST /api/settings/sensor
    Create a new sensor element. Json required:
      - description (string)
      - manufacturer (ManufacturerSettings)
      - ip (string)
      - api_key (string)
      - measuring_device (TankSettings)
      - measuring_position (number)
    """
    data = request.get_json() or {}
    required = ["description", "manufacturer", "ip", "api_key", "measuring_device", "measuring_position"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Missing fields: {', '.join(missing)}"), 422

    module = SensorSetting(
        description=data["description"],
        manufacturer=data["manufacturer"],
        ip=data["ip"],
        api_key=data["api_key"],
        measuring_device=data["measuring_device"],
        measuring_position=data["measuring_position"]
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/sensor/<int:module_id>", methods=["PUT"])
@jwt_required()
def update_sensor_module(module_id: int):
    """
    PUT /api/settings/sensor/<module_id>
    Update a new sensor element. Json required:
      - description (string)
      - manufacturer (ManufacturerSettings)
      - ip (string)
      - api_key (string)
      - measuring_device (TankSettings)
      - measuring_position (number)
    """
    module = SensorSetting.query.get_or_404(module_id)
    data = request.get_json() or {}

    for key in ("description", "manufacturer", "ip", "api_key", "measuring_device", "measuring_position"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200


@settings_bp.route("/sensor/<int:module_id>", methods=["DELETE"])
@jwt_required()
def delete_sensor_module(module_id):
    mod = SensorSetting.query.get_or_404(module_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204
