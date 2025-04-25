"""
Service zur Ansteuerung von Switchen.
Diese Logik kann GPIO, Relais-HAT oder Mock-Logik kapseln.
"""

from typing import Dict

# Dummy-Daten für Beispielzwecke
switch_states: Dict[int, bool] = {
    1: False,
    2: True
}


def get_switch_state(switch_id: int) -> bool:
    """
    Gibt den aktuellen Status eines Schalters zurück.
    """
    return switch_states.get(switch_id, False)


def toggle_switch(switch_id: int) -> bool:
    """
    Schaltet den angegebenen Switch um.
    """
    current_state = switch_states.get(switch_id, False)
    switch_states[switch_id] = not current_state
    print(f"[LOG] Switch {switch_id} toggled to {not current_state}")
    return True
