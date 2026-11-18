
import logging
from pathlib import Path


# --------------------------------------------------
# 1. PROJECT DIRECTORIES
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. CENTRALIZED LOGGER CONFIGURATION
# --------------------------------------------------

def get_logger(
    name="ingestion",
    log_file="ingestion.log",
    level=logging.INFO
):
    """
    Create and return a reusable logger.

    Logs are written to:
    1. Terminal (console)
    2. A log file inside the logs directory
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate log messages
    logger.propagate = False

    if not logger.handlers:

        # Common log format
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File handler
        file_path = LOG_DIR / log_file

        file_handler = logging.FileHandler(
            file_path,
            encoding="utf-8"
        )

        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()

        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        # Attach handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# --------------------------------------------------
# 3. LOGGING IMPLEMENTATION TEST
# --------------------------------------------------

if __name__ == "__main__":

    logger = get_logger(
        name="day23_logging_test",
        log_file="logging_test.log"
    )

    logger.debug("Debug message: Detailed execution information")

    logger.info("Ingestion process started successfully")

    logger.warning("Warning: Some records need validation")

    logger.error("Error: Sample error message")

    logger.critical("Critical: Sample critical message")

    logger.info("Logging implementation test completed")

    print("\nLogging Test Completed Successfully")
    print("Log file:", LOG_DIR / "logging_test.log")
