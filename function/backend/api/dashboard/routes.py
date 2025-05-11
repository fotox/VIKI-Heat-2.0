from flask import request

from flask import Blueprint, jsonify

from extensions import db, socketio
from database.dashboard import DashboardModuleSetting

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/modules", methods=["GET"])
def get_modules():
    modules = DashboardModuleSetting.query.all()
    return jsonify([{"id": m.id, "module_type": m.module_type} for m in modules])


@dashboard_bp.route("/modules", methods=["POST"])
def add_module():
    data = request.json
    module_type = data.get("module_type")
    new_module = DashboardModuleSetting(module_type=module_type, user_id=1)
    db.session.add(new_module)
    db.session.commit()
    return jsonify({"id": new_module.id, "module_type": new_module.module_type})


@dashboard_bp.route("/modules/<int:module_id>", methods=["DELETE"])
def remove_module(module_id):
    module = DashboardModuleSetting.query.get_or_404(module_id)
    db.session.delete(module)
    db.session.commit()
    return jsonify(success=True)
