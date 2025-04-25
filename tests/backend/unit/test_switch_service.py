from function.backend.services.switch_service import get_switch_state, toggle_switch


def test_get_switch_state_default_false():
    """Nicht gesetzter Switch gibt False"""
    assert get_switch_state(99) is False


def test_toggle_switch_changes_state():
    """Umschalten ändert Switch-State"""
    initial = get_switch_state(1)
    toggle_switch(1)
    assert get_switch_state(1) != initial
