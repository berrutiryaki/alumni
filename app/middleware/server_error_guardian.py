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
<html lang="en"><head><meta charset="UTF-8"><title>{code} Server Error</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Plus+Jakarta+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>body{{font-family:'Plus Jakarta Sans',sans-serif;background:#FAF8F5;color:#1C1917;display:flex;justify-content:center;padding-top:80px}}
.card{{background:#FFFFFF;border:1px solid #E7E5E4;padding:32px 40px;border-radius:10px;max-width:560px}}
h1{{font-family:'Playfair Display',serif;margin-top:0;color:#B91C1C}}a{{color:#1B4332;font-weight:600}}code{{background:#FAF8F5;border:1px solid #E7E5E4;padding:2px 6px;border-radius:4px}}</style></head>
<body><div class="card"><h1>{code} — Server Error</h1>
<p><b>Reason:</b> {reason}</p><p><b>Type:</b> <code>{error_type}</code></p>
<p><a href="/">&larr; Back to home</a></p></div></body></html>"""
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
