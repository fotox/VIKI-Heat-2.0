from flask import Blueprint, jsonify, request

from services.energy.tibber import pull_price_info_from_tibber_api
from services.energy.inverter import pull_live_data_from_inverter
from services.heating.helper import save_memory, load_memory, toggle_relay
from services.temperature.modbus_temp_module import read_temp_sensors_from_r4dcb08
from utils.logging_service import LoggingService

VALID_MODES = ["Automatik", "Manuell", "Schnell heizen", "Urlaub"]

modules_bp = Blueprint("modules", __name__, url_prefix="/api/dashboard")
logging = LoggingService()


# TODO: Refactor
@modules_bp.route("/energy_data", methods=["GET"])  # TODO: Refactor to live data
def get_energy_data():
    dummy_data = {
        f"'startsAt': '2025-07-03T{hour:02d}:00:00.000+02:00'": {
            "heating": 0.00,                            # TODO: Fill with heating manufacturer data
            "consumer": 0.00,                           # TODO: Fill with consumer manufacturer data
            "regular": 0.00,                            # TODO: Fill with regular manufacturer data (regular = consume - comsumer - heating)
            "production": round(2.0 + hour * 0.15, 2)   # TODO: Fill with Forecast or Sum-Production
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

    if price_information:  # Prüft ob die Liste nicht leer ist
        return jsonify(price_information), 200
    else:
        return jsonify([]), 204


@modules_bp.route("/heat_pipes", methods=["GET"])
def get_heat_pipe_states():
    """
    Get the current state from all the three heat pipes
    ---
    responses:
      200:
        description: State of all heat pipes [ON / OFF]
      500:
        description: State of all heat pipes not found
    """
    memory: dict = load_memory()
    heat_pipes: dict = memory.get("heat_pipes")
    try:
        return jsonify(heat_pipes), 200
    except KeyError:
        logging.error(f"[HEAT PIPE] Heat pipes not found in memory.")
        return jsonify({}), 500


@modules_bp.route("/heat_pipe/<int:pipe_id>", methods=["GET"])
def get_heat_pipe_state(pipe_id):
    """Get the current state from one of the three heat pipes"""
    if pipe_id not in [1, 2, 3]:
        return jsonify({"error": "Invalid pipe_id. Must be 1, 2, or 3"}), 400
    
    memory: dict = load_memory()
    heat_pipes = memory.get("heat_pipes", {})
    
    try:
        heat_pipe_state: bool = heat_pipes[str(pipe_id)]
        return jsonify({"pipe_id": pipe_id, "state": heat_pipe_state}), 200
    except KeyError:
        logging.error(f"[HEAT PIPE] Heat pipe {pipe_id} not found in memory.")
        return jsonify({"pipe_id": pipe_id, "state": False}), 404


@modules_bp.route("/heat_pipe/<int:pipe_id>", methods=["PUT"])
def toggle_heat_pipe(pipe_id: int):
    """Set the current state from one of the three heat pipes"""
    if pipe_id not in [1, 2, 3]:
        return jsonify({"error": "Invalid pipe_id. Must be 1, 2, or 3"}), 400
    
    data = request.get_json(silent=True) or {}
    state = data.get("state")

    if state is None:
        return jsonify({"error": "Missing 'state' in request body", "pipe_id": pipe_id}), 400
    
    if not isinstance(state, bool):
        return jsonify({"error": "'state' must be boolean (true/false)", "pipe_id": pipe_id}), 400

    new_state = toggle_relay(pipe_id, state)
    return jsonify({"pipe_id": pipe_id, "new_state": new_state}), 200


@modules_bp.route("/heating_mode", methods=["GET"])
def get_heating_mode():
    memory: dict = load_memory()
    mode: str = memory.get("mode")
    return jsonify({"mode": mode}), 200


@modules_bp.route("/heating_mode", methods=["PUT"])
def set_heating_mode():
    data: dict = request.get_json()
    
    if not data:
        return jsonify({"error": "Kein JSON Body"}), 400
    
    mode: str = data.get("mode")
    
    if not mode:
        return jsonify({"error": "Feld 'mode' fehlt"}), 400

    if mode not in VALID_MODES:
        return jsonify({"error": f"Ungültiger Modus. Erlaubt: {', '.join(VALID_MODES)}"}), 400

    memory: dict = load_memory()
    memory["mode"] = mode
    save_memory(memory)

    return jsonify({"message": "Modus aktualisiert", "mode": mode}), 200


@modules_bp.route("/inverter_data", methods=["GET"])
def get_inverter_data():
    return jsonify(pull_live_data_from_inverter()), 200


@modules_bp.route("/heating_tank_temp", methods=["GET"])
def get_heating_tank_temp():
    heating_tank_sensor_data: dict = read_temp_sensors_from_r4dcb08({0: 0.0, 1: 0.0, 2: 0.0})
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
    buffer_tank_sensor_data: dict = read_temp_sensors_from_r4dcb08({3: 0.0, 4: 0.0, 5: 0.0})
    sensor_data = {
        'dest_temp': 35.0,
        'sensor_1': buffer_tank_sensor_data[3],
        'sensor_2': buffer_tank_sensor_data[4],
        'sensor_3': buffer_tank_sensor_data[5],
        'heat_pipe': False
    }
    return jsonify(sensor_data), 200
