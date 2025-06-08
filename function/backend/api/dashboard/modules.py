from flask import Blueprint, jsonify, request

from services.energy.tibber import pull_price_info_from_tibber_api
from services.energy.inverter import pull_live_data_from_inverter
from services.temperature.modbus_temp_module import read_temp_sensors_from_r4dcb08

modules_bp = Blueprint("modules", __name__, url_prefix="/api/dashboard")

CURRENT_HEATING_MODE = {"mode": "Automatik"}
VALID_MODES = ["Automatik", "Manuell", "Schnell heizen", "Urlaub"]


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
    """
    Get the energy price from Tibber GraphQL
    ---
    responses:
      200:
        description: Tibber Price Information
        examples:
          application/json:
            {
              "today": [
                {"total": 0.3374, "startsAt": "2025-05-21T00:00:00.000+02:00"},
                {"total": 0.3307, "startsAt": "2025-05-21T01:00:00.000+02:00"}
              ]
            }
      204:
        description: Tibber Price Information not found
        examples:
          application/json:
            {
              "today": [],
              "tomorrow": []
            }
    """
    price_information: list = pull_price_info_from_tibber_api()

    if price_information is not []:
        return jsonify(price_information), 200
    else:
        return jsonify([]), 204


@modules_bp.route("/heat_pipe/<int:pipe_id>", methods=["GET"])
def get_heat_pipe_state(pipe_id):
    """
    Get the current state from one of the three heat pipes
    ---
    responses:
      200:
        description: State of heat pipe [ON / OFF]
        examples:
    """
    heat_pipe_state: str = 'HIGH'   # TODO: Refactor

    return jsonify({"pipe_id": pipe_id, "state": heat_pipe_state}), 200


@modules_bp.route("/heat_pipe/<int:pipe_id>", methods=["PUT"])
def toggle_heat_pipe(pipe_id):
    data = request.get_json()
    state = data.get("state", False)
    # heat_pipe_state: dict = switch_relay_state(pin_id=pipe_id, new_state=state)
    return jsonify({"pipe_id": pipe_id, "new_state": state}), 200


@modules_bp.route("/heating_mode", methods=["GET"])
def get_heating_mode():
    return jsonify({"mode": CURRENT_HEATING_MODE["mode"]}), 200


@modules_bp.route("/heating_mode", methods=["PUT"])
def set_heating_mode():
    data = request.get_json()
    mode = data.get("mode")

    if mode not in VALID_MODES:
        return jsonify({"error": "Ungültiger Modus"}), 400

    CURRENT_HEATING_MODE["mode"] = mode
    return jsonify({"message": "Modus aktualisiert", "mode": mode}), 200


@modules_bp.route("/inverter_data", methods=["GET"])
def get_inverter_data():
    return jsonify(pull_live_data_from_inverter(2)), 200  # TODO: Find a way to set id automatically


@modules_bp.route("/heating_tank_temp", methods=["GET"])
def get_heating_tank_temp():
    heating_tank_sensor_data: dict = read_temp_sensors_from_r4dcb08(dict.fromkeys(list(range(0, 3))))
    sensor_data = {
        'dest_temp': 60.0,
        'sensor_1': heating_tank_sensor_data[0],
        'sensor_2': heating_tank_sensor_data[1],
        'sensor_3': heating_tank_sensor_data[2],
        'heat_pipe': True
    }
    return jsonify(sensor_data), 200


@modules_bp.route("/buffer_tank_temp", methods=["GET"])
def get_buffer_tank_temp():
    buffer_tank_sensor_data: dict = read_temp_sensors_from_r4dcb08(dict.fromkeys(list(range(3, 6))))
    sensor_data = {
        'dest_temp': 35.0,
        'sensor_1': buffer_tank_sensor_data[3],
        'sensor_2': buffer_tank_sensor_data[4],
        'sensor_3': buffer_tank_sensor_data[5],
        'heat_pipe': False
    }
    return jsonify(sensor_data), 200
