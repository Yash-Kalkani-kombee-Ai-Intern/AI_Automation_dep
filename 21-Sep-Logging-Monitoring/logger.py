import logging
import os
from logging.handlers import RotatingFileHandler

LOG = "logs"

os.makedirs(LOG, exist_ok=True)

LOG_File = os.path.join(LOG, "app.log")

logger = logging.getLogger("monitoring")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handlers = RotatingFileHandler(
    LOG_File,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
)
file_handlers.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handlers)