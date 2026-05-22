import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class LoggerFactory:
    _instances: dict = {}
    _log_dir_created = False

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if name in cls._instances:
            return cls._instances[name]

        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        log_format = os.getenv("LOG_FORMAT", "json")

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level, logging.INFO))
        logger.handlers.clear()

        if log_format == "json":
            from pythonjsonlogger import jsonlogger
            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        else:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        log_file = os.getenv("LOG_FILE", "")
        if log_file:
            if not cls._log_dir_created:
                log_dir = os.path.dirname(log_file)
                if log_dir:
                    os.makedirs(log_dir, exist_ok=True)
                cls._log_dir_created = True

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        cls._instances[name] = logger
        return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name is None:
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            name = frame.f_back.f_globals.get("__name__", "unknown")
        else:
            name = "unknown"
    return LoggerFactory.get_logger(name)
