import sys

from services.heating.helper import (load_memory, all_relays, read_sensors_by_tank_with_heat_pipe,
                                     read_heat_pipe_config, save_memory)
from utils.logging_service import LoggingService

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    from services.heating.GpioMock import RPiGPIOSimulator
    GPIO = RPiGPIOSimulator()
else:
    import RPi.GPIO as GPIO

logging = LoggingService()

RELAY_PINS = {1: 20, 2: 21, 3: 26}
RELAY_PINS_CONFIG = read_heat_pipe_config()

GPIO.setmode(GPIO.BCM)
for pin in RELAY_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


# TODO: Manuell Mode funktioniert. Rest nicht.

def automatic_control(cover: int):
    memory: dict = load_memory()
    mode: str = memory.get("mode")
    sensors: dict = read_sensors_by_tank_with_heat_pipe()
    temp: float = sensors.get("tank")[2]
    dest_temp = sensors.get("dest_temp", 0)

    if mode == "Automatik":
        if temp >= dest_temp:
            logging.debug("Automatic mode: Temp higher than dest temp. All relays turned off.")
            all_relays(RELAY_PINS, False)
        else:
            total_on = 0
            for i in range(1, 4):
                phase = RELAY_PINS_CONFIG.get(f"phase_{i}", 0)
                buffer = RELAY_PINS_CONFIG.get(f"buffer_{i}", 0)
                pin = RELAY_PINS[i]
                logging.debug(f"[Automatic mode] Cover: {cover} | Phase {i}: {phase + buffer}")
                if cover > phase + buffer:
                    logging.debug(f"[Automatic mode] Turn phase {i} on")
                    GPIO.output(pin, GPIO.HIGH)
                    cover -= (phase + buffer)
                    total_on += 1
                elif cover < 0:
                    logging.debug(f"[Automatic mode] Turn phase {i} off")
                    GPIO.output(pin, GPIO.LOW)

    elif mode == "Urlaub":
        all_relays(RELAY_PINS, True)

    elif mode == "Schnell heizen":
        if temp >= dest_temp:
            all_relays(RELAY_PINS, False)
        else:
            all_relays(RELAY_PINS, True)


def switch_relay_state(pin: int, new_state: bool) -> bool:
    memory: dict = load_memory()
    mode: str = memory.get("mode")
    state: bool = memory.get("heat_pipe")[str(pin)]
    if mode == "Manuell":
        if new_state:
            GPIO.output(pin, GPIO.HIGH)
            memory["heat_pipe"][str(pin)] = new_state
        else:
            GPIO.output(pin, GPIO.LOW)
            memory["heat_pipe"][str(pin)] = new_state

        save_memory(memory)
    return new_state
