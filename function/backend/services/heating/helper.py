import json
import sys
import requests

from services.temperature.modbus_temp_module import read_temp_sensors_from_r4dcb08
from database.crud import fetch_heat_pipe_setting

IS_WINDOWS = sys.platform == "win32"
MODE_FILE = "mode_state.json"

if IS_WINDOWS:
    from services.heating.GpioMock import RPiGPIOSimulator
    GPIO = RPiGPIOSimulator()
else:
    import RPi.GPIO as GPIO


def load_mode() -> dict:
    try:
        with open(MODE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"mode": "automatic", "deactivated_until": None}


def save_mode(state: dict) -> None:
    with open(MODE_FILE, 'w') as f:
        json.dump(state, f)


def get_json(url: str) -> dict:
    try:
        r = requests.get(url, timeout=3)
        return r.json()
    except BaseException:
        return {}


def all_relays(relay_pins: dict, state: bool) -> None:
    for phase, pin in relay_pins.items():
        GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
    if IS_WINDOWS:
        display_relay_states(relay_pins)


def display_relay_states(relay_pins: dict):
    states = {phase: GPIO.pins[pin]['state'] for phase, pin in relay_pins.items()}
    print("[Simulator] Aktuelle Relay-Zustände:", states)


def read_sensors_by_tank_with_heat_pipe() -> tuple[dict, float]:
    heating_tank: dict = read_temp_sensors_from_r4dcb08(dict.fromkeys(list(range(0, 3))))
    buffer_tank: dict = read_temp_sensors_from_r4dcb08(dict.fromkeys(list(range(3, 6))))

    sensors: dict = {}
    dest_temp: float = 0.0

    return sensors, dest_temp


def read_heat_pipe_config() -> dict:
    fetch_heat_pipe_setting()
