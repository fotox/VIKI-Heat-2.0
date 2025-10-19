from flask import request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from database.settings import ManufacturerCategorySetting
from . import settings_bp


@settings_bp.route("/category", methods=["GET"])
def list_category_modules():
    """
    GET /api/settings/category
    Return all category-modules as list.
    :return: All existed modules
    """
    categories = ManufacturerCategorySetting.query.order_by(ManufacturerCategorySetting.description).all()
    return jsonify(categories=[m.to_dict() for m in categories]), 200


@settings_bp.route("/category/<int:category_id>", methods=["GET"])
def category_module_by_id(category_id):
    """
    GET /api/settings/category/<int:category_id>
    Return category-module by id.
    :return: Manufacturer-module
    """
    categories = ManufacturerCategorySetting.query.get_or_404(category_id)
    return jsonify(categories.to_dict()), 200


@settings_bp.route("/category", methods=["POST"])
@jwt_required()
def create_category_module():
    """
    POST /api/settings/category
    Create new category-module. Wait for JSON with:
      - description (string)
      - category (string)
    :return: Created module
    """
    data = request.get_json() or {}
    required = ["description", "category"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(msg=f"Missing fields: {', '.join(missing)}"), 422

    module = ManufacturerCategorySetting(
        description=data["description"],
        category=data["category"],
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@settings_bp.route("/category/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category_module(category_id: int):
    """
    PUT /api/settings/category/<category_id>
    Update one of existed category-modules.
    JSON can be contained one of the following items:
      - description (string)
      - category (string)
    :param: Identifier of the module
    :return: Updated module
    """
    module = ManufacturerCategorySetting.query.get_or_404(category_id)
    data = request.get_json() or {}

    for key in ("description", "category"):
        if key in data:
            setattr(module, key, data[key])

    db.session.commit()
    return jsonify(module.to_dict()), 200


@settings_bp.route("/category/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category_module(category_id):
    """
    DELETE /api/settings/category/<category_id>
    DELETE one of existed category-modules.
    :param category_id: Identifier of the module
    :return: Empty string
    """
    mod = ManufacturerCategorySetting.query.get_or_404(category_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204
