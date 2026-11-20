"""
5xx Guardian middleware — catches every server error (500, 502, 503 ...) and
responds with the reason instead of a bare "Internal Server Error".

- /api/* paths  -> JSON:  {"status": "error", "code": 500, "reason": "...", "error_type": "...", "path": "..."}
- other paths   -> small HTML error page showing the same reason

The full traceback is always printed to the terminal for debugging.
"""

import logging
import traceback

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from app.middleware.error_log import log_error

logger = logging.getLogger("5xx-guardian")


def _describe(error: Exception) -> tuple:
    """Return (status_code, error_type, reason) for any exception."""
    if isinstance(error, HTTPException):
        code = error.code or 500
        reason = error.description or error.name
    else:
        code = 500
        reason = str(error) or "An unexpected error occurred while processing the request."
    return code, type(error).__name__, reason


def init_server_error_guardian(app: Flask) -> None:
    """Register 5xx handlers on the given Flask app."""

    def _respond(error):
        code, error_type, reason = _describe(error)

        # Always show the traceback in the terminal.
        print(f"[5xx] {request.method} {request.path} -> {code} {error_type}: {reason}", flush=True)
        original = getattr(error, "original_exception", None) or error
        traceback.print_exception(type(original), original, original.__traceback__)
        log_error(code, request.method, request.path, f"{error_type}: {reason}",
                  exc_info=(type(original), original, original.__traceback__))

        if request.path.startswith("/api/"):
            return jsonify({
                "status": "error",
                "code": code,
                "reason": reason,
                "error_type": error_type,
                "method": request.method,
                "path": request.path,
            }), code

        html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>{code} Server Error — Alumni Platform</title>
<link href="https://fonts.googleapis.com/css2?family=Boldonse&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/static/css/theme.css">
</head>
<body>
<section class="band-dark hero" style="min-height:85vh;display:flex;align-items:center;">
<div class="orb orb-a"></div>
<div class="container">
<span class="announce-pill"><span><b>{code} Guardian</b> &middot; {error_type}</span></span>
<h1 class="display-md" style="margin-top:24px;">Server <span class="accent">error</span>.</h1>
<div class="card-light" style="max-width:560px;margin:28px auto 0;text-align:left;">
<p style="font-weight:600;margin-bottom:8px;">Reason</p>
<p style="color:#57534E;">{reason}</p>
</div>
<div style="margin-top:28px;"><a href="/" class="btn btn-sprout btn-lg">Back to home</a></div>
</div></section></body></html>"""
        return html, code, {"Content-Type": "text/html; charset=utf-8"}

    # Any 5xx raised via abort(5xx) or returned by Flask itself.
    for status in (500, 501, 502, 503, 504):
        app.register_error_handler(status, _respond)

    # Any unhandled exception (would otherwise become a bare 500).
    @app.errorhandler(Exception)
    def _handle_unexpected(error):
        if isinstance(error, HTTPException) and (error.code or 500) < 500:
            return error  # 4xx are not ours; let their own handlers deal with them
        return _respond(error)
