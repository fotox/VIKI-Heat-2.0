import json

from services.temperature.modbus_temp_module import read_temp_sensors_from_r4dcb08
from utils.logging_service import LoggingService
MEMORY_FILE = "memory.json"

logging = LoggingService()
RELAY_PINS: dict = {1: 20, 2: 21, 3: 26}


def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo') as f:
            return 'raspberrypi' in f.read().lower()
    except BaseException:
        return False


IS_RPi: bool = is_raspberry_pi()


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
    gpio = get_gpio()
    try:
        memory: dict = load_memory()

        for pin in RELAY_PINS:
            gpio.output(RELAY_PINS[pin], gpio.HIGH if state else gpio.LOW)
            memory["heat_pipes"][str(pin)] = state

        save_memory(memory)

    except Exception as err:
        logging.error(f"[ToggleAllRelais] Failed to toogle relay: {err}")


def toogle_relay(pin: int, state: bool) -> bool:
    gpio = get_gpio()
    try:
        memory: dict = load_memory()
        if memory["heat_pipes"][str(pin)] != state:
            gpio.output(RELAY_PINS[pin], gpio.HIGH if state else gpio.LOW)
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


def get_gpio():
    if IS_RPi:
        import RPi.GPIO as GPIO
    else:
        from services.heating.GpioMock import RPiGPIOSimulator
        GPIO = RPiGPIOSimulator()

    return GPIO


def init_gpio():
    GPIO = get_gpio()

    GPIO.setmode(GPIO.BCM)
    for pin in RELAY_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
