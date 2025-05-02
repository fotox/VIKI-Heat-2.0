from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from database.settings import HeatingSetting
from . import settings_bp


@settings_bp.route("/heating", methods=["GET"])
def list_heating_modules():
    """
    GET /api/settings/heating
    Return all heating-modules as list.
    :return: All existed modules
    """
    modules = HeatingSetting.query.order_by(HeatingSetting.id).all()
    return jsonify(modules=[m.to_dict() for m in modules]), 200


@settings_bp.route("/heating", methods=["POST"])
@jwt_required()
def create_heating_module():
    """
    POST /api/settings/heating
    Create new heating-module. Wait for JSON with:
      - system_id (string)
      - manufacturer (ManufacturerSetting)
      - ip (string)
      - url (string)
      - api (string)
      - price (number)
      - power_factor (number)
      - selected (boolean)
    :return: Created module
    """
    data = request.get_json() or {}
    required = ["system_id", "manufacturer", "ip", "url", "api", "price", "power_factor", "selected"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Missing fields: {', '.join(missing)}"), 422

    module = HeatingSetting(
        system_id=data["system_id"],
        manufacturer=data["manufacturer"],
        ip=data["ip"],
        url=data["url"],
        api=data["api"],
        price=data["price"],
        power_factor=data["power_factor"],
        selected=data["selected"]
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/heating/<int:module_id>", methods=["PUT"])
@jwt_required()
def update_heating_module(module_id: int):
    """
    PUT /api/settings/heating/<module_id>
    Update one of existed heating-modules.
    JSON can be contained one of the following items:
      - system_id (string)
      - manufacturer (ManufacturerSetting)
      - ip (string)
      - url (string)
      - api (string)
      - price (number)
      - power_factor (number)
      - selected (boolean)
    :param: Identifier of the module
    :return: Updated module
    """
    module = HeatingSetting.query.get_or_404(module_id)
    data = request.get_json() or {}

    for key in ("system_id", "manufacturer", "ip", "url", "api", "price", "power_factor", "selected"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200


@settings_bp.route("/heating/<int:module_id>", methods=["DELETE"])
@jwt_required()
def delete_heating_module(module_id):
    """
    DELETE /api/settings/heating/<module_id>
    DELETE one of existed heating-modules.
    :param module_id: Identifier of the module
    :return: Empty string
    """
    mod = HeatingSetting.query.get_or_404(module_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204
