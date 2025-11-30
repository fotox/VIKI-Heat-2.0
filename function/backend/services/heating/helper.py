import json
import threading

from services.temperature.modbus_temp_module import read_temp_sensors_from_r4dcb08
from utils.logging_service import LoggingService

MEMORY_FILE = "memory.json"
_memory_lock = threading.Lock()
DEV_MODE: bool = False

logging = LoggingService()
RELAY_PINS: dict = {1: 20, 2: 21, 3: 26}


def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo') as f:
            return 'raspberry' in f.read().lower()
    except BaseException:
        return False


IS_RPi: bool = is_raspberry_pi()


def load_memory() -> dict:
    with _memory_lock:
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"[MEMORY] Mode file not found: {MEMORY_FILE}")
            # Erstelle Default-Memory wenn nicht vorhanden
            default_memory = {
                "heat_pipes": {"1": False, "2": False, "3": False},
                "mode": "Automatik"
            }
            save_memory(default_memory)
            return default_memory


def save_memory(memory: dict) -> None:
    with _memory_lock:
        try:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2, ensure_ascii=False)
        except (FileNotFoundError, IOError) as e:
            logging.error(f"[MEMORY] Error saving memory file: {e}")


def toggle_all_relais(state: bool) -> None:
    gpio = get_gpio()
    try:
        memory: dict = load_memory()

        for pin in RELAY_PINS:
            gpio.output(RELAY_PINS[pin], not state)
            memory["heat_pipes"][str(pin)] = state

        save_memory(memory)

    except Exception as err:
        logging.error(f"[TOGGLEALLRELAIS] Failed to toggle relay: {err}")


def toggle_relay(pin: int, state: bool) -> bool:
    gpio = get_gpio()
    
    if pin not in RELAY_PINS:
        logging.error(f"[TOGGLERELAY] Invalid pin: {pin}")
        return False
        
    try:
        memory: dict = load_memory()
        
        if not memory.get("heat_pipes"):
            logging.error("[TOGGLERELAY] Heat pipes not initialized in memory")
            return False

        if memory["heat_pipes"].get(str(pin)) != state:
            gpio.output(RELAY_PINS[pin], not state)
            memory["heat_pipes"][str(pin)] = state
            save_memory(memory)
            logging.info(f"[TOGGLERELAY] Pipe {pin} set to {state}")
            return state
        else:
            logging.debug(f"[TOGGLERELAY] Pipe {pin} already in state {state}")
            return state

    except (KeyError, TypeError, ValueError) as err:
        logging.error(f"[TOGGLERELAY] Failed to toggle relay {pin}: {err}")
        return False


def read_sensors_by_tank_with_heat_pipe() -> dict:
    # TODO: Add selector to get active heat pipe tank
    tank_with_sensor = 0

    if tank_with_sensor == 0:
        tank: dict = read_temp_sensors_from_r4dcb08({0: 0.0, 1: 0.0, 2: 0.0})
        dest_temp: float = 50.0  # TODO: Load from database
    else:
        tank: dict = read_temp_sensors_from_r4dcb08({3: 0.0, 4: 0.0, 5: 0.0})
        dest_temp: float = 35.0  # TODO: Load from database

    # DEBUG Modus nur wenn gewünscht:
    if DEV_MODE and False:  # Explizit deaktiviert, aktiviere mit True
        tank = {0: 25.7, 1: 38.4, 2: 49.1}
        logging.debug("[SENSORS] Using DEBUG data")

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
        GPIO.output(pin, True)
