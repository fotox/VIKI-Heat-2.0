"""
Service zur Abfrage von Temperatur-Sensoren via 1-Wire.
"""

import glob
from typing import Optional


class SensorService:
    def __init__(self, base_dir: str = "/sys/bus/w1/dashboard/"):
        self.base_dir = base_dir

    def get_sensor_ids(self) -> list[str]:
        """Liefert alle angeschlossenen 1-Wire-IDs"""
        return [d.split("/")[-1] for d in glob.glob(f"{self.base_dir}28-*")]

    def read_temperature_raw(self, sensor_id: str) -> list[str]:
        """Liest Rohdaten eines Sensors"""
        try:
            with open(f"{self.base_dir}{sensor_id}/w1_slave", "r") as f:
                return f.readlines()
        except FileNotFoundError:
            return []

    def read_temperature(self, sensor_id: str) -> Optional[float]:
        """Parst Temperatur aus Sensordaten"""
        lines = self.read_temperature_raw(sensor_id)
        if len(lines) < 2 or "YES" not in lines[0]:
            return None
        temp_line = lines[1].split("t=")
        if len(temp_line) < 2:
            return None
        return round(float(temp_line[1]) / 1000.0, 2)

    def read_all_temperatures(self) -> dict:
        """Liest alle Temperaturen der Sensoren"""
        sensors = self.get_sensor_ids()
        return {
            sid: self.read_temperature(sid)
            for sid in sensors
        }
