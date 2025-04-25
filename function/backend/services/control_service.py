"""
Logik zur Steuerung von Betriebsmodi & automatischer Entscheidung.
"""

from typing import Optional


class ControlService:
    def __init__(self):
        self.mode: str = "auto"  # oder "manual"

    def set_mode(self, mode: str) -> bool:
        """Setzt Steuerungsmodus"""
        if mode in ("auto", "manual"):
            self.mode = mode
            return True
        return False

    def get_mode(self) -> str:
        """Gibt aktuellen Modus zurück"""
        return self.mode

    def should_activate_switch(self, temperature: float, forecast: Optional[float] = None) -> bool:
        """
        Entscheidungsregel: Aktiviere z. B. bei zu niedriger Temp oder schlechtem Forecast.
        """
        if self.mode != "auto":
            return False
        return temperature < 19 or (forecast is not None and forecast < 20)
