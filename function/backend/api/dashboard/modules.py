from flask import Blueprint, jsonify, request

from services.energy.tibber import pull_price_info_from_tibber_api
from services.energy.inverter import pull_live_data_from_inverter

modules_bp = Blueprint("modules", __name__, url_prefix="/api/dashboard")


@modules_bp.route("/energy_data", methods=["GET"])  # TODO: Refactor to live data
def get_energy_data():
    dummy_data = {
        f"{hour:02d}": {
            "heating": round(0.5 + hour * 0.1, 2),
            "consumer": round(0.7 + hour * 0.05, 2),
            "regular": round(0.2 + hour * 0.02, 2),
            "production": round(2.0 + hour * 0.15, 2)
        }
        for hour in range(24)
    }
    return jsonify(dummy_data)


@modules_bp.route("/energy_price", methods=["GET"])
def get_energy_price():
    return jsonify(pull_price_info_from_tibber_api())


@modules_bp.route("/heat_pipe/<int:pipe_id>", methods=["GET"])
def heat_pipe(pipe_id):
    state = pipe_id % 2 == 0
    return jsonify({"pipe_id": pipe_id, "state": state})


@modules_bp.route("/heat_pipe/<int:pipe_id>", methods=["PUT"])
def toggle_heat_pipe(pipe_id):
    data = request.get_json()
    state = data.get("state", False)
    return jsonify({"pipe_id": pipe_id, "new_state": state})


@modules_bp.route("/inverter_data", methods=["GET"])
def get_inverter_data():
    return jsonify(pull_live_data_from_inverter(2))     # TODO: Find a way to set id automatically


@modules_bp.route("/heating_tank_temp", methods=["GET"])
def get_heating_tank_temp():
    dummy_data = {
        'dest_temp': 60.0,
        'sensor_1': 41.81,
        'sensor_2': 42.25,
        'sensor_3': None
    }
    return jsonify(dummy_data)


@modules_bp.route("/buffer_tank_temp", methods=["GET"])
def get_buffer_tank_temp():
    dummy_data = {
        'dest_temp': 35.0,
        'sensor_1': 19.0,
        'sensor_2': 23.06,
        'sensor_3': 28.06
    }
    return jsonify(dummy_data)
