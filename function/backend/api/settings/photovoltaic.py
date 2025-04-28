from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from services.settings import PhotovoltaicSetting
from . import settings_bp


@settings_bp.route("/photovoltaic", methods=["GET"])
def list_photovoltaic_modules():
    """
    GET /api/settings/photovoltaik
    Liefert alle PV-Module als Liste.
    """
    modules = PhotovoltaicSetting.query.order_by(PhotovoltaicSetting.id).all()
    return jsonify(modules=[m.to_dict() for m in modules]), 200


@settings_bp.route("/photovoltaic", methods=["POST"])
@jwt_required()
def create_photovoltaic_module():
    """
    POST /api/settings/photovoltaik
    Legt ein neues PV-Modul an. Erwartet JSON mit mindestens:
      - system_id (string)
      - location (string)
      - max_output (number)
    """
    data = request.get_json() or {}
    # Mindestfelder prüfen
    required = ["system_id", "location", "max_output"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Fehlende Felder: {', '.join(missing)}"), 422

    module = PhotovoltaicSetting(
        system_id=data["system_id"],
        location=data["location"],
        max_output=data["max_output"]
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/photovoltaic/<int:module_id>", methods=["PUT"])
@jwt_required()
def update_photovoltaic_module(module_id: int):
    """
    PUT /api/settings/photovoltaik/<module_id>
    Aktualisiert ein bestehendes PV-Modul.
    JSON kann eines oder mehrere dieser Felder enthalten:
      - system_id, location, max_output
    """
    module = PhotovoltaicSetting.query.get_or_404(module_id)
    data = request.get_json() or {}

    for key in ("system_id", "location", "max_output"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200
