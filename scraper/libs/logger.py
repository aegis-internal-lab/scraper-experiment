import logging

from scraper.configs.constants import LOG_LEVEL, LOGGER_FILE_NAME

formatter = logging.Formatter(
    "%(asctime)s : %(name)s  : %(funcName)s : %(levelname)s : %(message)s"
)

logger = logging.getLogger(__name__)
handler = logging.FileHandler(LOGGER_FILE_NAME)

handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(LOG_LEVEL)
