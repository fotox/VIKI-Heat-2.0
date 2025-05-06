from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from database.settings import LocationSetting
from . import settings_bp


@settings_bp.route("/location", methods=["GET"])
def list_manufacturer_modules():
    """
    GET /api/settings/location
    Return all location-modules as list.
    :return: All existed modules
    """
    locations = LocationSetting.query.order_by(LocationSetting.description).all()
    return jsonify(locations=[m.to_dict() for m in locations]), 200


@settings_bp.route("/location/<int:location_id>", methods=["GET"])
def manufacturer_module_by_id(location_id):
    """
    GET /api/settings/location/<int:location_id>
    Return location-module by id.
    :return: Location-module
    """
    locations = LocationSetting.query.get_or_404(location_id)
    return jsonify(locations.to_dict()), 200


@settings_bp.route("/location", methods=["POST"])
@jwt_required()
def create_location_module():
    """
    POST /api/settings/location
    Create new location-module. Wait for JSON with:
      - description (string)
      - latitude (number)
      - longitude (number)
      - city_code (number)
      - city (string)
      - street (string)
      - street_number (number)
    :return: Created module
    """
    data = request.get_json() or {}
    required = ["description", "latitude", "longitude", "city_code", "city", "street", "street_number"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Missing fields: {', '.join(missing)}"), 422

    module = LocationSetting(
        description=data["description"],
        location=data["location"],
        model_type=data["model_type"],
        url=data["url"],
        api=data["api"],
        power_factor=data["power_factor"],
        power_size=data["power_size"]
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/location/<int:location_id>", methods=["PUT"])
@jwt_required()
def update_location_module(location_id: int):
    """
    PUT /api/settings/location/<location_id>
    Update one of existed location-modules.
    JSON can be contained one of the following items:
      - description (string)
      - latitude (number)
      - longitude (number)
      - city_code (number)
      - city (string)
      - street (string)
      - street_number (number)
    :param: Identifier of the module
    :return: Updated module
    """
    module = LocationSetting.query.get_or_404(location_id)
    data = request.get_json() or {}

    for key in ("description", "latitude", "longitude", "city_code", "city", "street", "street_number"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200


@settings_bp.route("/location/<int:location_id>", methods=["DELETE"])
@jwt_required()
def delete_location_module(location_id):
    """
    DELETE /api/settings/location/<location_id>
    DELETE one of existed location-modules.
    :param location_id: Identifier of the module
    :return: Empty string
    """
    mod = LocationSetting.query.get_or_404(location_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204
