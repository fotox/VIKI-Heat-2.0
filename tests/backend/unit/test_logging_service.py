from function.backend.utils.logging_service import LoggingService


def test_logging_does_not_crash():
    log = LoggingService()
    log.info("Info test")
    log.warning("Warn test")
    log.error("Error test")
