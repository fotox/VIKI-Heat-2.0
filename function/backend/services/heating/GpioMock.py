import time
import threading

from utils.logging_service import LoggingService

logging = LoggingService()


class RPiGPIOSimulator:
    BCM = 'BCM'
    BOARD = 'BOARD'
    IN = 'IN'
    OUT = 'OUT'
    HIGH = 1
    LOW = 0
    PUD_UP = 'PUD_UP'
    PUD_DOWN = 'PUD_DOWN'
    FALLING = 'FALLING'
    RISING = 'RISING'
    BOTH = 'BOTH'

    def __init__(self):
        self.mode = None
        self.pins = {pin: {'mode': None, 'state': None, 'pull': None, 'callbacks': []} for pin in range(1, 41)}
        self.pwm_instances = {}
        self.running = True
        self.warnings = True
        self.event_thread = threading.Thread(target=self._event_loop, daemon=True)
        self.event_thread.start()

    def setmode(self, mode):
        if mode not in [self.BCM, self.BOARD]:
            logging.error("Invalid mode. Use RPiGPIOSimulator.BCM or RPiGPIOSimulator.BOARD")
            raise ValueError("Invalid mode. Use RPiGPIOSimulator.BCM or RPiGPIOSimulator.BOARD")
        self.mode = mode

    def setwarnings(self, state):
        if not isinstance(state, bool):
            logging.error("Invalid state. State must be a boolean.")
            raise ValueError("State must be a boolean")
        self.warnings = state

    def setup(self, pin, mode, pull=None):
        if pin not in self.pins:
            logging.error(f"Invalid GPIO pin: {pin}")
            raise ValueError("Invalid GPIO pin")
        self.pins[pin]['mode'] = mode
        self.pins[pin]['pull'] = pull

        if mode == self.OUT:
            self.pins[pin]['state'] = self.LOW
        elif mode == self.IN and pull == self.PUD_UP:
            self.pins[pin]['state'] = self.HIGH
        elif mode == self.IN and pull == self.PUD_DOWN:
            self.pins[pin]['state'] = self.LOW

    def output(self, pin, state):
        if pin not in self.pins:
            logging.error(f"Pin {pin} not set as OUTPUT.")
            raise ValueError("Pin not set as OUTPUT")
        self.pins[pin]['state'] = state

    def input(self, pin):
        if pin not in self.pins:
            logging.error(f"Pin {pin} not set as INPUT.")
            raise ValueError("Pin not set as INPUT")
        return self.pins[pin]['state']

    def add_event_detect(self, pin, edge, callback):
        if pin not in self.pins or self.pins[pin]['mode'] != self.IN:
            logging.error(f"Pin {pin} not set as INPUT.")
            raise ValueError("Pin not set as INPUT")
        self.pins[pin]['callbacks'].append((edge, callback))

    def _event_loop(self):
        while self.running:
            for pin, config in self.pins.items():
                if config['mode'] == self.IN:
                    for edge, callback in config['callbacks']:
                        if edge == self.RISING and config['state'] == self.HIGH:
                            callback(pin)
                        elif edge == self.FALLING and config['state'] == self.LOW:
                            callback(pin)
            time.sleep(0.01)

    def cleanup(self):
        self.running = False
        self.event_thread.join()
        self.pins = {pin: {'mode': None, 'state': None, 'pull': None, 'callbacks': []} for pin in range(1, 41)}
        logging.info("Cleanup complete")
