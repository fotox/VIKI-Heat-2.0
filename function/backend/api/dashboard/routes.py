from flask import request
from flask import Blueprint, jsonify

from extensions import db, socketio
from database.dashboard import DashboardModuleSetting

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/modules", methods=["GET"])
def get_modules():
    modules = DashboardModuleSetting.query.all()
    return jsonify([{"id": m.id, "module_type": m.module_type, "position": m.position} for m in modules])


@dashboard_bp.route("/modules", methods=["POST"])
def add_module():
    data = request.json
    module_type = data.get("module_type")
    new_module = DashboardModuleSetting(module_type=module_type, user_id=1)
    db.session.add(new_module)
    db.session.commit()
    return jsonify({"id": new_module.id, "module_type": new_module.module_type, "position": new_module.position})


@dashboard_bp.route("/modules/<int:module_id>", methods=["DELETE"])
def remove_module(module_id):
    module = DashboardModuleSetting.query.get_or_404(module_id)
    db.session.delete(module)
    db.session.commit()
    return jsonify(success=True)


@dashboard_bp.route("/modules/reorder", methods=["POST"])
def reorder_modules():
    data = request.json
    if not isinstance(data, list):
        return jsonify({"error": "Ungültiges Format, erwartetes Array von Objekten"}), 400

    try:
        for item in data:
            module_id = item.get("id")
            position = item.get("position")

            if module_id is None or position is None:
                return jsonify({"error": f"Ungültige Datenstruktur: {item}"}), 400

            module = DashboardModuleSetting.query.get(module_id)
            if not module:
                return jsonify({"error": f"Modul mit ID {module_id} nicht gefunden"}), 404

            module.position = position

        db.session.commit()
        return jsonify({"message": "Positionen erfolgreich aktualisiert"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
