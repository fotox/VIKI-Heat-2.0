from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from database.settings import EnergySetting
from . import settings_bp


@settings_bp.route("/energy", methods=["GET"])
def list_energy_modules():
    """
    GET /api/settings/energy
    Return all energy-modules as list.
    :return: All existed modules
    """
    modules = EnergySetting.query.order_by(EnergySetting.id).all()
    return jsonify(modules=[m.to_dict() for m in modules]), 200


@settings_bp.route("/energy", methods=["POST"])
@jwt_required()
def create_energy_module():
    """
    POST /api/settings/energy
    Create new energy-module. Wait for JSON with:
      - system_id (string)
      - manufacturer (ManufacturerSetting)
      - ip (string)
      - api_key (string)
      - price (number)
    :return: Created module
    """
    data = request.get_json() or {}
    required = ["description", "manufacturer", "ip", "api_key", "price"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Missing fields: {', '.join(missing)}"), 422

    module = EnergySetting(
        description=data["description"],
        manufacturer=data["manufacturer"],
        ip=data["ip"],
        api_key=data["api_key"],
        price=data["price"]
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/energy/<int:module_id>", methods=["PUT"])
@jwt_required()
def update_energy_module(module_id: int):
    """
    PUT /api/settings/energy/<module_id>
    Update one of existed energy-modules.
    JSON can be contained one of the following items:
      - system_id (string)
      - manufacturer (ManufacturerSetting)
      - ip (string)
      - api_key (string)
      - price (number)
    :param: Identifier of the module
    :return: Updated module
    """
    module = EnergySetting.query.get_or_404(module_id)
    data = request.get_json() or {}

    for key in ("description", "manufacturer", "ip", "api_key", "price"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200


@settings_bp.route("/energy/<int:module_id>", methods=["DELETE"])
@jwt_required()
def delete_energy_module(module_id):
    """
    DELETE /api/settings/energy/<module_id>
    DELETE one of existed energy-modules.
    :param module_id: Identifier of the module
    :return: Empty string
    """
    mod = EnergySetting.query.get_or_404(module_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204
