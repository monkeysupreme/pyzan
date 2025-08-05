import logging
import sys
from datetime import datetime

class Logger:
    def __init__(self, module: str, log_file: str = "app.logs", level=logging.INFO):
        self.module = module.upper()

        self.logger = logging.getLogger(self.module)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            formatter = logging.Formatter(
                f"[%(asctime)s][{self.module}] %(message)s", "%Y-%m-%d %H:%M:%S"
            )

            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # File handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)
