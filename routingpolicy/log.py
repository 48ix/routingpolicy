"""Logging instance setup & configuration."""

# Standard Library
import os
import sys

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
    """Initialize hyperglass logging instance."""
    _loguru_logger.remove()
    _loguru_logger.add(sys.stdout, format=_LOG_FMT, level="INFO", enqueue=True)
    _loguru_logger.configure(levels=_LOG_LEVELS)  # type: ignore
    return _loguru_logger


log = base_logger()


def set_log_level(logger: LoguruLogger, debug: bool) -> bool:
    """Set log level based on debug state."""
    if debug:
        os.environ["HYPERGLASS_AGENT_LOG_LEVEL"] = "DEBUG"
        logger.remove()
        logger.add(sys.stdout, format=_LOG_FMT, level="DEBUG", enqueue=True)
        logger.configure(levels=_LOG_LEVELS)

    if debug:
        logger.debug("Debugging enabled")
    return True
