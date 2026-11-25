"""
Role-Based Access Control (RBAC) & 403 Guardian middleware.
Enforces the role permissions defined in ddd.md across web routes.
"""

from functools import wraps
from flask import Flask, abort, redirect, render_template, request, session, url_for
from werkzeug.exceptions import Forbidden

from app.middleware.error_log import log_error
from app.models.user import User


def get_current_user() -> User | None:
    user_id = session.get("user_id")
    return User.get_by_id(user_id) if user_id else None


def require_roles(*allowed_roles: str):
    """
    Decorator that restricts a web route to users whose role is in allowed_roles.
    - Unauthenticated visitors (guest) are redirected to /login.
    - Authenticated users without an allowed role receive a 403 Forbidden response
      explaining their current role and the required roles per ddd.md.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if user is None:
                return redirect(url_for("auth.login_form"))

            user_role = (user.role or user.status or "student").lower()
            if user_role not in allowed_roles:
                allowed_str = ", ".join(r.capitalize() for r in allowed_roles)
                abort(
                    403,
                    description=(
                        f"Your current role is '{user_role.capitalize()}'. "
                        f"This action is restricted to: {allowed_str}."
                    ),
                )
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def init_forbidden_guardian(app: Flask) -> None:
    """Register the 403 Forbidden error handler on the Flask app."""

    @app.errorhandler(403)
    def _handle_403(error: Forbidden):
        user = get_current_user()
        user_role = (user.role or user.status) if user else "guest"
        reason = (
            error.description
            if error and error.description
            else "You do not have permission to perform this action."
        )
        log_error(403, request.method, request.path, f"[{user_role}] {reason}")
        return (
            render_template(
                "403.html",
                reason=reason,
                requested_path=request.path,
                user_role=user_role,
            ),
            403,
        )
