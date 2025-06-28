import json
import sys

from services.temperature.modbus_temp_module import read_temp_sensors_from_r4dcb08
from database.fetch_data import fetch_heat_pipe_setting
from utils.logging_service import LoggingService

IS_WINDOWS = sys.platform == "win32"
MEMORY_FILE = "memory.json"

logging = LoggingService()

if IS_WINDOWS:
    from services.heating.GpioMock import RPiGPIOSimulator
    GPIO = RPiGPIOSimulator()
else:
    import RPi.GPIO as GPIO


def load_memory() -> dict:
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"[MEMORY] Mode file not found: {MEMORY_FILE}")
        return dict()


def save_memory(memory: dict) -> None:
    try:
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory, f)
    except FileNotFoundError:
        logging.error(f"[MEMORY] Mode file not found: {MEMORY_FILE}")


def all_relays(relay_pins: dict, state: bool) -> None:
    memory: dict = load_memory()
    for phase, pin in relay_pins.items():
        GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
        memory.get("heat_pipe")[pin] = state
    if IS_WINDOWS:
        states = {phase: GPIO.pins[pin]['state'] for phase, pin in relay_pins.items()}
        logging.info(f"[Simulator] Current relay states: {states}")


# TODO: Build tank temp function
def read_sensors_by_tank_with_heat_pipe() -> dict:
    # TODO: Add selector to get active heat pipe tank
    tank_with_sensor = 0

    if tank_with_sensor == 0:
        tank: dict = read_temp_sensors_from_r4dcb08(dict.fromkeys(list(range(0, 3))))
        dest_temp: float = 50.0  # TODO: Load from database

    else:
        tank: dict = read_temp_sensors_from_r4dcb08(dict.fromkeys(list(range(3, 6))))
        dest_temp: float = 35.0  # TODO: Load from database

    # TODO: DEBUG DEV
    tank: dict = {0: 25.7, 1: 38.4, 2: 49.1}

    return {"tank": tank, "dest_temp": dest_temp}


def read_heat_pipe_config() -> dict:
    return fetch_heat_pipe_setting()
