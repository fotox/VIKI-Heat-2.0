from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.switch_service import get_switch_state, toggle_switch
from extensions import db, socketio

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/", methods=["GET"])
def list_devices() -> tuple:
    """Liefert Geräte mit aktuellem Status"""
    devices = [
        {"id": 1, "name": "Heizung", "state": get_switch_state(1)},
        {"id": 2, "name": "Pumpe", "state": get_switch_state(2)},
        {"id": 3, "name": "Lüftung", "state": get_switch_state(1)},
    ]
    return jsonify(devices=devices), 200


@dashboard_bp.route("/<int:switch_id>/toggle", methods=["POST"])
@jwt_required()
def toggle_device(switch_id: int) -> tuple:
    """Schaltet Gerät um (nur Admins erlaubt)"""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify(msg="Nur Admins dürfen Geräte umschalten"), 403

    new_state = toggle_switch(switch_id)
    if new_state is not None:
        socketio.emit(
            'switch_updated',
            {'id': switch_id, 'new_state': new_state}
        )
        return jsonify(msg=f"Switch {switch_id} geschaltet"), 200

    return jsonify(msg="Fehler beim Schalten"), 500
