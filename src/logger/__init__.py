import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Constants for log configuration
LOG_DIR = "logs"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Number of backup log files to keep

# Use the current working directory instead of from_root()
project_root = os.getcwd()
log_dir_path = os.path.join(project_root, LOG_DIR)
log_file_path = os.path.join(log_dir_path, LOG_FILE)

# Make sure the logs folder exists
os.makedirs(log_dir_path, exist_ok=True)


def configure_logger():
    """
    Configures logging with a rotating file handler and a console handler.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Create and expose the logger
logger = configure_logger()
