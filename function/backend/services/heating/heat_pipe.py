import time
import sys
from datetime import datetime, timedelta

from services.heating.helper import (load_mode, get_json, save_mode, all_relays, display_relay_states,
                                     read_sensors_by_tank_with_heat_pipe, read_heat_pipe_config)

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    from services.heating.GpioMock import RPiGPIOSimulator
    GPIO = RPiGPIOSimulator()
else:
    import RPi.GPIO as GPIO

RELAY_PINS = {1: 20, 2: 21, 3: 26}
LOG_FILE = "relay_controller.log"
CHECK_INTERVAL = 1

GPIO.setmode(GPIO.BCM)
for pin in RELAY_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def run_loop():
    while True:
        now = datetime.now()
        mode_state = load_mode()
        mode = mode_state["mode"]

        if mode == "automatic" and mode_state.get("deactivated_until"):
            until = datetime.fromisoformat(mode_state["deactivated_until"])
            if now >= until:
                mode_state["deactivated_until"] = None
                save_mode(mode_state)

        inverter = get_json("http://localhost/api/modules/inverter_data")
        config = read_heat_pipe_config()
        sensors, dest_temp = read_sensors_by_tank_with_heat_pipe()

        cover = inverter.get("cover", 0)
        temp = sensors.get("temp", 0)

        if mode == "holidays":
            all_relays(RELAY_PINS, False)

        elif mode == "fast":
            if temp >= dest_temp:
                all_relays(RELAY_PINS, False)
                mode_state["deactivated_until"] = (now + timedelta(days=1)).replace(hour=6, minute=0, second=0,
                                                                                    microsecond=0).isoformat()
                save_mode(mode_state)
            else:
                all_relays(RELAY_PINS, True)

        elif mode == "manual":
            pass

        elif mode == "automatic":
            if temp >= dest_temp:
                all_relays(RELAY_PINS, False)
                mode_state["deactivated_until"] = (now + timedelta(days=1)).replace(hour=6, minute=0, second=0,
                                                                                    microsecond=0).isoformat()
                save_mode(mode_state)
            else:
                total_on = 0
                for i in range(1, 4):
                    phase = config.get(f"phase_{i}", 0)
                    buffer = config.get(f"buffer_{i}", 0)
                    pin = RELAY_PINS[i]
                    if cover > phase + buffer:
                        GPIO.output(pin, GPIO.HIGH)
                        cover -= (phase + buffer)
                        total_on += 1
                    elif cover < 0:
                        GPIO.output(pin, GPIO.LOW)
                if IS_WINDOWS:
                    display_relay_states(RELAY_PINS)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_loop()
