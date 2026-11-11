"""
Error file logger — appends 404 / 5xx errors to logs/error.logs.

Line format:
    2026-11-11 10:38:22 | 404 | GET  | /api/job-postingz | reason...
5xx entries are followed by the full traceback.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "error.logs")

_logger = logging.getLogger("alumni.error_file")
_logger.setLevel(logging.INFO)
_logger.propagate = False  # keep it out of the terminal; the terminal has its own logger

if not _logger.handlers:
    os.makedirs(LOG_DIR, exist_ok=True)
    _handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    _handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    _logger.addHandler(_handler)


def log_error(code: int, method: str, path: str, reason: str, exc_info=None) -> None:
    """Append one error entry to logs/error.logs (never raises)."""
    try:
        _logger.error(f"{code} | {method:<6} | {path} | {reason}", exc_info=exc_info)
    except Exception:
        pass
