"""
Logger middleware — prints one line per request to the terminal.

Format:
    time        method   route                 status   duration
    10:20:30    POST     /user                 201      18ms
"""

import logging
import time
from datetime import datetime

from flask import Flask, g, request

_HEADER = f"{'time':<10}  {'method':<7}  {'route':<30}  {'status':<6}  duration"


def init_logger(app: Flask) -> None:
    """Register request logging hooks on the given Flask app."""

    # Silence werkzeug's default access log so only our format is shown.
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    state = {"header_printed": False}

    @app.before_request
    def _start_timer():
        g._request_start = time.perf_counter()

    @app.after_request
    def _log_request(response):
        start = getattr(g, "_request_start", None)
        duration_ms = int((time.perf_counter() - start) * 1000) if start is not None else 0

        if not state["header_printed"]:
            print(_HEADER, flush=True)
            state["header_printed"] = True

        print(
            f"{datetime.now().strftime('%H:%M:%S'):<10}  "
            f"{request.method:<7}  "
            f"{request.path:<30}  "
            f"{response.status_code:<6}  "
            f"{duration_ms}ms",
            flush=True,
        )
        return response
