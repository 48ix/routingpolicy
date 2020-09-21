"""Logging instance setup & configuration."""

# Standard Library
import os
import sys
from pathlib import Path

# Third Party
from loguru import logger as _loguru_logger
from loguru import _Logger as LoguruLogger  # type: ignore

_LOG_FMT = (
    "<lvl><b>[{level}]</b> {time:YYYYMMDD} {time:HH:mm:ss} <lw>|</lw> {name}<lw>:</lw>"
    "<b>{line}</b> <lw>|</lw> {function}</lvl> <lvl><b>→</b></lvl> {message}"
)
_LOG_LEVELS = [
    {"name": "TRACE", "color": "<m>"},
    {"name": "DEBUG", "color": "<c>"},
    {"name": "INFO", "color": "<le>"},
    {"name": "SUCCESS", "color": "<g>"},
    {"name": "WARNING", "color": "<y>"},
    {"name": "ERROR", "color": "<y>"},
    {"name": "CRITICAL", "color": "<r>"},
]


def base_logger() -> LoguruLogger:
    """Initialize logging instance."""
    _loguru_logger.remove()
    _loguru_logger.add(sys.stdout, format=_LOG_FMT, level="INFO", enqueue=True)
    _loguru_logger.configure(levels=_LOG_LEVELS)  # type: ignore
    return _loguru_logger


log = base_logger()


def setup_logging(
    logger: LoguruLogger, debug: bool, logfile: Path, logsize: str
) -> bool:
    """Set log level based on debug state."""
    level = "INFO"

    if debug:
        level = "DEBUG"
    os.environ["48IX_ROUTING_POLICY_LOG_LEVEL"] = level

    logger.remove()
    logger.add(sys.stdout, format=_LOG_FMT, level=level, enqueue=True)
    logger.add(logfile, rotation=logsize, level=level, enqueue=True)
    logger.configure(levels=_LOG_LEVELS)

    if debug:
        logger.debug("Debugging enabled")
    return True
