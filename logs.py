import os

from loguru import logger
class LogManager:
    def __init__(self, log_file):
        log_directory = os.path.dirname(os.path.abspath(__file__))
        log_directory = os.path.join(log_directory, "logs")
        log_path = os.path.join(log_directory, f"{log_file}.log")
        self.log_handler = logger.add(log_path)

    def log(self, level, message):
        # Directly use logger to log the message
        if level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
        # ... you can add more levels as needed

    def close_log(self):
        # Remove the file handler if you need to
        logger.remove(self.log_handler)
