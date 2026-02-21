import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
    log_file = "bot_activity.log"

    # 5MB per file, keeping 5 old backups
    rotating_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=5
    )
    rotating_handler.setFormatter(log_formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[rotating_handler, stream_handler]
    )
