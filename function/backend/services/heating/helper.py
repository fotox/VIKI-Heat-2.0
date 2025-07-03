import json
import sys

from services.temperature.modbus_temp_module import read_temp_sensors_from_r4dcb08
from utils.logging_service import LoggingService

IS_WINDOWS = sys.platform == "win32"
MEMORY_FILE = "memory.json"

logging = LoggingService()

if IS_WINDOWS:
    from services.heating.GpioMock import RPiGPIOSimulator
    GPIO = RPiGPIOSimulator()
else:
    import RPi.GPIO as GPIO


RELAY_PINS = {1: 20, 2: 21, 3: 26}

GPIO.setmode(GPIO.BCM)
for pin in RELAY_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


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


def toggle_all_relais(state: bool) -> None:
    try:
        memory: dict = load_memory()

        for pin in RELAY_PINS:
            GPIO.output(RELAY_PINS[pin], GPIO.HIGH if state else GPIO.LOW)
            memory["heat_pipes"][str(pin)] = state

        save_memory(memory)

    except Exception as err:
        logging.error(f"[ToggleAllRelais] Failed to toogle relay: {err}")


def toogle_relay(pin: int, state: bool) -> bool:
    try:
        memory: dict = load_memory()
        if memory["heat_pipes"][str(pin)] != state:
            GPIO.output(RELAY_PINS[pin], GPIO.HIGH if state else GPIO.LOW)
            memory["heat_pipes"][str(pin)] = state

            save_memory(memory)
            return state
        else:
            return not state

    except Exception as err:
        logging.error(f"[ToggleRelay] Failed to toogle relay: {err}")
        return not state


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
