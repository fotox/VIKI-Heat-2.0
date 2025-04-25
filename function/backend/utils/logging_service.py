"""
Einfacher Logging-Service für strukturierte Ausgaben.
Künftig auch erweiterbar für Datei- oder Remote-Logging.
"""

import datetime


class LoggingService:
    def __init__(self, prefix: str = "VIKI"):
        self.prefix = prefix

    def log(self, message: str, level: str = "INFO") -> None:
        """Gibt eine formatierte Log-Meldung aus"""
        timestamp = datetime.datetime.now().isoformat(timespec="seconds")
        print(f"[{self.prefix}] [{timestamp}] [{level}] {message}")

    def info(self, message: str) -> None:
        self.log(message, "INFO")

    def warning(self, message: str) -> None:
        self.log(message, "WARN")

    def error(self, message: str) -> None:
        self.log(message, "ERROR")
