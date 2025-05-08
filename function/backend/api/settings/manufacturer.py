from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from database.settings import ManufacturerSetting
from . import settings_bp


@settings_bp.route("/manufacturer", methods=["GET"])
def list_manufacturer_modules():
    """
    GET /api/settings/manufacturer
    Return all manufacturer-modules as list.
    :return: All existed modules
    """
    manufacturers = ManufacturerSetting.query.order_by(ManufacturerSetting.description).all()
    return jsonify(manufacturers=[m.to_dict() for m in manufacturers]), 200


@settings_bp.route("/manufacturer/<int:module_id>", methods=["GET"])
def manufacturer_module_by_id(module_id):
    """
    GET /api/settings/manufacturer/<int:module_id>
    Return manufacturer-module by id.
    :return: Manufacturer-module
    """
    manufacturers = ManufacturerSetting.query.get_or_404(module_id)
    return jsonify(manufacturers.to_dict()), 200


@settings_bp.route("/manufacturer", methods=["POST"])
@jwt_required()
def create_manufacturer_module():
    """
    POST /api/settings/manufacturer
    Create new manufacturer-module. Wait for JSON with:
      - description (string)
      - manufacturer (string)
      - model_type (string)
      - url (string)
      - api (string)
      - power_factor (number)
      - power_size (number)
    :return: Created module
    """
    data = request.get_json() or {}
    required = ["description", "manufacturer", "model_type", "url", "api", "power_factor", "power_size"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Missing fields: {', '.join(missing)}"), 422

    module = ManufacturerSetting(
        description=data["description"],
        manufacturer=data["manufacturer"],
        model_type=data["model_type"],
        url=data["url"],
        api=data["api"],
        power_factor=data["power_factor"],
        power_size=data["power_size"]
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/manufacturer/<int:module_id>", methods=["PUT"])
@jwt_required()
def update_manufacturer_module(module_id: int):
    """
    PUT /api/settings/manufacturer/<module_id>
    Update one of existed manufacturer-modules.
    JSON can be contained one of the following items:
      - description (string)
      - manufacturer (string)
      - model_type (string)
      - url (string)
      - api (string)
      - power_factor (number)
      - power_size (number)
    :param: Identifier of the module
    :return: Updated module
    """
    module = ManufacturerSetting.query.get_or_404(module_id)
    data = request.get_json() or {}

    for key in ("description", "manufacturer", "model_type", "url", "api", "power_factor", "power_size"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200


@settings_bp.route("/manufacturer/<int:module_id>", methods=["DELETE"])
@jwt_required()
def delete_manufacturer_module(module_id):
    """
    DELETE /api/settings/manufacturer/<module_id>
    DELETE one of existed manufacturer-modules.
    :param module_id: Identifier of the module
    :return: Empty string
    """
    mod = ManufacturerSetting.query.get_or_404(module_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204
