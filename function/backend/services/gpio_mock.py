"""
Mock-Modul zur GPIO-Simulation für Windows und Entwicklung ohne Hardware.
Nutzt interne Dummies anstelle der RPi.GPIO-Bibliothek.
"""


class GPIO:
    BCM = "BCM"
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0

    _pin_state = {}

    @staticmethod
    def setmode(mode):
        print(f"[GPIO-MOCK] setmode({mode})")

    @staticmethod
    def setup(pin, mode):
        GPIO._pin_state[pin] = GPIO.LOW
        print(f"[GPIO-MOCK] setup(pin={pin}, mode={mode})")

    @staticmethod
    def output(pin, state):
        GPIO._pin_state[pin] = state
        print(f"[GPIO-MOCK] output(pin={pin}, state={state})")

    @staticmethod
    def input(pin):
        return GPIO._pin_state.get(pin, GPIO.LOW)

    @staticmethod
    def cleanup():
        print("[GPIO-MOCK] cleanup()")
        GPIO._pin_state.clear()
