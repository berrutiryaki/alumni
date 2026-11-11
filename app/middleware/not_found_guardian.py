"""
404 Guardian middleware — catches every 404, logs the reason, and:
- for /api/* paths: returns JSON 404 with reason & suggestions
- for web paths:    redirects invalid requests to the generic /404 page
"""

import difflib

from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.exceptions import NotFound

from app.middleware.error_log import log_error

# Werkzeug's stock description; if we see it, no custom reason was supplied.
_DEFAULT_DESCRIPTION = NotFound.description


def _static_routes(app: Flask) -> list:
    """Collect route patterns without dynamic parts, for 'did you mean' hints."""
    routes = set()
    for rule in app.url_map.iter_rules():
        if rule.endpoint in ("static", "not_found_page") or "<" in rule.rule:
            continue
        routes.add(rule.rule.rstrip("/") or "/")
    return sorted(routes)


def _get_suggestions(app: Flask, path: str) -> list:
    target = (path or "").rstrip("/") or "/"
    return difflib.get_close_matches(target, _static_routes(app), n=3, cutoff=0.6)


def _build_reason(error: NotFound, path: str) -> str:
    # A route/controller used abort(404, "reason") -> keep that reason.
    if error and error.description and error.description != _DEFAULT_DESCRIPTION:
        return error.description
    return f"No route matches '{path}'. The URL does not exist on this server."


def init_not_found_guardian(app: Flask) -> None:
    """Register the generic /404 page route and 404 error handler on the Flask app."""

    @app.route("/404", methods=["GET"])
    def not_found_page():
        requested_path = request.args.get("path", "")
        reason = request.args.get("reason") or (
            f"No route matches '{requested_path}'. The URL does not exist on this server."
            if requested_path
            else "The requested page or resource does not exist."
        )
        suggestions = _get_suggestions(app, requested_path) if requested_path else []
        return (
            render_template(
                "404.html",
                reason=reason,
                requested_path=requested_path,
                suggestions=suggestions,
            ),
            404,
        )

    @app.errorhandler(404)
    def _handle_404(error):
        reason = _build_reason(error, request.path)
        log_error(404, request.method, request.path, reason)
        suggestions = _get_suggestions(app, request.path)

        if request.path.startswith("/api/"):
            body = {
                "status": "error",
                "code": 404,
                "reason": reason,
                "method": request.method,
                "path": request.path,
            }
            if suggestions:
                body["suggestions"] = suggestions
            return jsonify(body), 404

        # Redirect invalid web requests to the generic /404 page
        return redirect(url_for("not_found_page", path=request.path, reason=reason))
