import logging
from logging.handlers import RotatingFileHandler

# Global variable to track verbose state
console_handler = None

def setup_logging():
    global console_handler
    log_format = '%(asctime)s [%(levelname)s]: %(message)s'
    formatter = logging.Formatter(log_format)

    # 1. File Handler (Permanent Logs)
    file_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING) # Only log warnings/errors to file

    # 2. Console Handler (Live Feedback)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO) # Start with rolls visible

    # 3. Attach handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Silence discord.py internal noise
    logging.getLogger('discord').setLevel(logging.ERROR)
