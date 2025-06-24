import datetime
import os


class LoggingService:
    def __init__(self, prefix: str = "VIKI", log_file: str = None):
        """
        :param prefix: Präfix für die Logzeile
        :param log_file: Pfad zur Logdatei (standard: ..\\logs\\system.log relativ zur Skriptdatei)
        """
        if log_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            log_file = os.path.abspath(os.path.join(base_dir, "..", "logs", "system.log"))

        self.prefix = prefix
        self.log_file = log_file

        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, "a", encoding="utf-8"):
            pass

    def log(self, message: str, level: str = "INFO") -> None:
        """Gibt eine formatierte Log-Meldung aus und schreibt sie in eine Datei"""
        timestamp = datetime.datetime.now().isoformat(timespec="seconds")
        formatted = f"[{self.prefix}] [{timestamp}] [{level}] {message}"

        print(formatted)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

    def info(self, message: str) -> None:
        self.log(message, "INFO")

    def warning(self, message: str) -> None:
        self.log(message, "WARN")

    def error(self, message: str) -> None:
        self.log(message, "ERROR")
