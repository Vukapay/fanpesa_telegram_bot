"""
FanPesa Telegram Bot Logging Configuration

This module configures application-wide structured logging.

Features:
- Console logging (development)
- JSON logging (production)
- Rotating log files
- Configurable log levels
- Ready for Docker & Kubernetes
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path

from pythonjsonlogger.json import JsonFormatter

from app.config.settings import settings

# -----------------------------------------------------------------------------
# Log Directory
# -----------------------------------------------------------------------------

LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(exist_ok=True)

LOG_FILE = LOG_DIRECTORY / "fanpesa.log"

# -----------------------------------------------------------------------------
# Logger Name
# -----------------------------------------------------------------------------

LOGGER_NAME = "fanpesa"

# -----------------------------------------------------------------------------
# JSON Formatter
# -----------------------------------------------------------------------------

JSON_FORMAT = JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(filename)s %(funcName)s %(lineno)d %(message)s"
)

# -----------------------------------------------------------------------------
# Console Formatter
# -----------------------------------------------------------------------------

CONSOLE_FORMAT = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# -----------------------------------------------------------------------------
# Logger Factory
# -----------------------------------------------------------------------------


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Returns a configured logger.

    Example:

        logger = get_logger(__name__)

        logger.info("Application started")
    """

    logger = logging.getLogger(name or LOGGER_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level.upper())

    # -------------------------------------------------------------------------
    # Console Handler
    # -------------------------------------------------------------------------

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CONSOLE_FORMAT)

    logger.addHandler(console_handler)

    # -------------------------------------------------------------------------
    # Rotating File Handler
    # -------------------------------------------------------------------------

    file_handler = logging.handlers.RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(JSON_FORMAT)

    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# -----------------------------------------------------------------------------
# Default Application Logger
# -----------------------------------------------------------------------------

logger = get_logger()
