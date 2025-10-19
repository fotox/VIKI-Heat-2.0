from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from database.settings import TankSetting
from . import settings_bp


@settings_bp.route("/tank", methods=["GET"])
def list_tank_modules():
    """
    GET /api/settings/tank
    Return list of tank modules.
    """
    modules = TankSetting.query.order_by(TankSetting.id).all()
    return jsonify(modules=[m.to_dict() for m in modules]), 200


@settings_bp.route("/tank", methods=["POST"])
@jwt_required()
def create_tank_module():
    """
    POST /api/settings/tank
    Create a new tank element. Json required:
      - description (string)
      - volume (number)
    """
    data = request.get_json() or {}
    required = ["description", "volume"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Missing fields: {', '.join(missing)}"), 422

    module = TankSetting(
        description=data["description"],
        volume=data["volume"]
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/tank/<int:module_id>", methods=["PUT"])
@jwt_required()
def update_tank_module(module_id: int):
    """
    PUT /api/settings/tank/<module_id>
    Update a new tank element. Json required:
      - description (string)
      - volume (number)
    """
    module = TankSetting.query.get_or_404(module_id)
    data = request.get_json() or {}

    for key in ("description", "volume"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200


@settings_bp.route("/tank/<int:module_id>", methods=["DELETE"])
@jwt_required()
def delete_tank_module(module_id):
    mod = TankSetting.query.get_or_404(module_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204
