import datetime
import os


class LoggingService:
    """
    Simple logging service for structured console and file output.

    Supports logging at different severity levels (INFO, DEBUG, WARN, ERROR) and writes
    to a default or user-defined log file.
    """

    def __init__(self, prefix: str = "VIKI", log_file: str = None):
        if log_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            log_file = os.path.abspath(os.path.join(base_dir, "..", "logs", "system.log"))

        self.prefix = prefix
        self.log_file = log_file

        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, "a", encoding="utf-8"):
            pass

    def log(self, message: str, level: str = "INFO") -> None:
        """
        Logs a message with a given severity level to the console and the log file.

        Args:
            message (str): The log message to record.
            level (str): The log level (e.g., "INFO", "DEBUG", "WARN", "ERROR").
        """
        timestamp = datetime.datetime.now().isoformat(timespec="seconds")
        formatted = f"[{self.prefix}] [{timestamp}] [{level}] {message}"

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

    def info(self, message: str) -> None:
        self.log(message, "INFO")

    def debug(self, message: str) -> None:
        self.log(message, "DEBUG")

    def warning(self, message: str) -> None:
        self.log(message, "WARN")

    def error(self, message: str) -> None:
        self.log(message, "ERROR")
