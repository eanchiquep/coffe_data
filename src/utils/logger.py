"""
Logging utilities
"""

import logging
from config.settings import LOG_LEVEL, LOG_FORMAT, LOGS_PATH

LOGS_PATH.mkdir(exist_ok=True)


def get_logger(name):
    """Get configured logger"""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # File handler
    file_handler = logging.FileHandler(LOGS_PATH / f"{name}.log")
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
