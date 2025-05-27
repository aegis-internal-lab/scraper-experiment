import logging
import sys
from pathlib import Path

from scraper.configs.constants import LOG_LEVEL, LOGGER_FILE_NAME


def setup_logger(name: str = __name__) -> logging.Logger:
    """Setup and return a configured logger"""
    formatter = logging.Formatter(
        "%(asctime)s : %(name)s : %(funcName)s : %(levelname)s : %(message)s"
    )

    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # File handler
    log_file = Path(LOGGER_FILE_NAME)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    return logger


# Default logger instance
logger = setup_logger(__name__)
