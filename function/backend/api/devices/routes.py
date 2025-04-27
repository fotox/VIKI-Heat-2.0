"""
Routen zur Steuerung und Abfrage von Geräten (Schalter).
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.switch_service import get_switch_state, toggle_switch

devices_bp = Blueprint("devices", __name__)


@devices_bp.route("/", methods=["GET"])
@jwt_required()
def list_devices() -> tuple:
    """Liefert Geräte mit aktuellem Status"""
    devices = [
        {"id": 1, "name": "Heizung", "state": get_switch_state(1)},
        {"id": 2, "name": "Pumpe", "state": get_switch_state(2)},
    ]
    return jsonify(devices=devices), 200


@devices_bp.route("/<int:switch_id>/toggle", methods=["POST"])
@jwt_required()
def toggle_device(switch_id: int) -> tuple:
    """Schaltet Gerät um (nur Admins erlaubt)"""
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify(msg="Nur Admins dürfen Geräte umschalten"), 403

    success = toggle_switch(switch_id)
    if success:
        return jsonify(msg=f"Switch {switch_id} geschaltet"), 200
    return jsonify(msg="Fehler beim Schalten"), 500
