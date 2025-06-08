from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from database.settings import PhotovoltaicSetting
from . import settings_bp


@settings_bp.route("/photovoltaic", methods=["GET"])
def list_photovoltaic_modules():
    """
    GET /api/settings/photovoltaic
    Liefert alle PV-Module als Liste.
    """
    modules = PhotovoltaicSetting.query.order_by(PhotovoltaicSetting.id).all()
    return jsonify(modules=[m.to_dict() for m in modules]), 200


# TODO: Standort und neues Tabellenschema einbinden

@settings_bp.route("/photovoltaic", methods=["POST"])
@jwt_required()
def create_photovoltaic_module():
    """
    POST /api/settings/photovoltaic
    Legt ein neues PV-Modul an. Erwartet JSON mit mindestens:
      - description (string)
      - manufacturer (ManufacturerSettings)
      - duration (number)
      - angle (number)
      - module_count (number)
      - location (LocationSettings)
    """
    data = request.get_json() or {}
    required = ["description", "manufacturer", "duration", "angle", "module_count", "location"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Missing fields: {', '.join(missing)}"), 422

    module = PhotovoltaicSetting(
        description=data["description"],
        manufacturer=data["manufacturer"],
        duration=data["duration"],
        angle=data["angle"],
        module_count=data["module_count"],
        location=data["location"]
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/photovoltaic/<int:module_id>", methods=["PUT"])
@jwt_required()
def update_photovoltaic_module(module_id: int):
    """
    PUT /api/settings/photovoltaic/<module_id>
    Aktualisiert ein bestehendes PV-Modul.
    JSON kann eines oder mehrere dieser Felder enthalten:
      - description (string)
      - manufacturer (ManufacturerSettings)
      - duration (number)
      - angle (number)
      - module_count (number)
      - location (LocationSettings)
    """
    module = PhotovoltaicSetting.query.get_or_404(module_id)
    data = request.get_json() or {}

    for key in ("description", "manufacturer", "duration", "angle", "module_count", "location"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200


@settings_bp.route("/photovoltaic/<int:module_id>", methods=["DELETE"])
@jwt_required()
def delete_photovoltaic_module(module_id):
    mod = PhotovoltaicSetting.query.get_or_404(module_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204
