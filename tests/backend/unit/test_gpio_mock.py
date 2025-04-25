from function.backend.services.gpio_mock import GPIO


def test_gpio_setmode():
    """Testet setmode"""
    GPIO.setmode(GPIO.BCM)
    # Keine Exception = OK


def test_gpio_setup_and_output():
    """Testet setup und output"""
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.HIGH)
    assert GPIO.input(17) == GPIO.HIGH


def test_gpio_input_default_low():
    """Testet Standardwert (LOW) für nicht gesetzte Pins"""
    assert GPIO.input(99) == GPIO.LOW


def test_gpio_cleanup():
    """Testet cleanup der Pins"""
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)
    GPIO.cleanup()
    assert GPIO.input(27) == GPIO.LOW
