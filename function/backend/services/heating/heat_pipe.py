import sys

from services.heating.helper import (load_mode, all_relays, display_relay_states, read_sensors_by_tank_with_heat_pipe,
                                     read_heat_pipe_config)

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    from services.heating.GpioMock import RPiGPIOSimulator
    GPIO = RPiGPIOSimulator()
else:
    import RPi.GPIO as GPIO

RELAY_PINS = {1: 20, 2: 21, 3: 26}
RELAY_PINS_CONFIG = read_heat_pipe_config()

GPIO.setmode(GPIO.BCM)
for pin in RELAY_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def automatic_control(cover: int):
    mode = load_mode()
    sensors, dest_temp = read_sensors_by_tank_with_heat_pipe()
    temp = sensors.get("temp", 0)

    if mode == "Urlaub":
        all_relays(RELAY_PINS, True)

    elif mode == "Schnell heizen":
        if temp >= dest_temp:
            all_relays(RELAY_PINS, False)
        else:
            all_relays(RELAY_PINS, True)

    elif mode == "Manuell":
        pass

    elif mode == "Automatik":
        if temp >= dest_temp:
            all_relays(RELAY_PINS, False)
        else:
            total_on = 0
            for i in range(1, 4):
                phase = RELAY_PINS_CONFIG.get(f"phase_{i}", 0)
                buffer = RELAY_PINS_CONFIG.get(f"buffer_{i}", 0)
                pin = RELAY_PINS[i]
                if cover > phase + buffer:
                    GPIO.output(pin, GPIO.HIGH)
                    cover -= (phase + buffer)
                    total_on += 1
                elif cover < 0:
                    GPIO.output(pin, GPIO.LOW)
            if IS_WINDOWS:
                display_relay_states(RELAY_PINS)
