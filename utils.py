import logging
from config import LOG_FORMAT, LOG_FILE, LOG_LEVEL

def check_none(value):
    return '' if value is None else str(value)

def setup_logging():
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    logger = logging.getLogger('request_app')
    logger.setLevel(log_level)
    
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(log_level)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()