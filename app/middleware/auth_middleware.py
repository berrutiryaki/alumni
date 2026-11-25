"""
Auth Middleware — central authentication and role-based authorization (RBAC) middleware.

Responsibilities:
1. Identity Resolution (@app.before_request):
   - Reads session['user_id'] (web) or 'X-User-Id' / 'Authorization: Bearer <id>' header (API).
   - Populates `g.current_user` and `g.current_role` ('guest', 'student', 'alumni', 'academician', 'admin').
2. Route Gatekeeper (@app.before_request):
   - Blocks unauthenticated ('guest') access to protected routes/methods (redirects web to /login, returns 401 JSON for protected API).
   - Enforces the ddd.md Role Permission Matrix centrally across all modules (returns 403 Forbidden when a role is not permitted).
3. Response Headers & Context (@app.after_request & @app.context_processor):
   - Injects `current_user` and `current_role` into all Jinja2 templates.
   - Adds `X-Auth-Role` header to HTTP responses for visibility.
4. Decorators & Error Handlers:
   - Provides `@login_required` and `@require_roles(*roles)` decorators.
   - Handles 401 Unauthorized and 403 Forbidden for both HTML and `/api/*` JSON routes.
"""

from functools import wraps
from flask import Flask, abort, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.exceptions import Forbidden, Unauthorized

from app.middleware.error_log import log_error
from app.models.user import User

# Public path prefixes that never require authentication
PUBLIC_PREFIXES = (
    "/static/",
    "/flasgger_static/",
    "/api/swagger",
    "/api/health",
)

# Public exact paths allowed for guests
PUBLIC_EXACT_PATHS = {
    "/",
    "/about",
    "/hello",
    "/login",
    "/register",
    "/logout",
    "/404",
}


def is_admin(user: User | None) -> bool:
    """Strictly check whether the given user has the 'admin' role."""
    return bool(user is not None and (user.role or "").strip().lower() == "admin")


def get_current_user() -> User | None:
    """
    Return the authenticated User strictly from session['user_id'] (or API headers on /api/*).
    Never falls back to User.query.first() or any default user.
    """
    if hasattr(g, "current_user"):
        return g.current_user

    user_id = session.get("user_id")
    if not user_id and request.path.startswith("/api/"):
        # Header-based user ID is allowed ONLY on /api/* endpoints for Postman testing
        header_uid = request.headers.get("X-User-Id")
        auth_header = request.headers.get("Authorization", "")
        if not header_uid and auth_header.lower().startswith("bearer "):
            header_uid = auth_header.split(" ", 1)[1].strip()
        if header_uid and str(header_uid).isdigit():
            user_id = int(header_uid)

    if not user_id:
        return None
    try:
        user = User.get_by_id(int(user_id))
        if user is None and "user_id" in session:
            session.pop("user_id", None)
        return user
    except Exception:
        return None


def get_current_role() -> str:
    """Return the active normalized lowercase role ('guest', 'student', 'alumni', 'academician', 'admin')."""
    if hasattr(g, "current_role"):
        return g.current_role
    user = get_current_user()
    if user is None:
        return "guest"
    return (user.role or "student").strip().lower()


def login_required(fn):
    """Decorator requiring an authenticated user session (non-guest)."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user is None:
            log_error(401, request.method, request.path, "[guest] Authentication required")
            if request.path.startswith("/api/"):
                return jsonify({
                    "status": "error",
                    "code": 401,
                    "reason": "Authentication required. Please log in or provide X-User-Id header.",
                    "role": "guest",
                    "path": request.path,
                }), 401
            return redirect(url_for("auth.login_form", next=request.path))
        return fn(*args, **kwargs)
    return wrapper


def require_roles(*allowed_roles: str):
    """
    Decorator restricting a route to specific roles defined in ddd.md.
    - Guest -> Redirects to /login (web) or 401 JSON (API).
    - Logged-in user without allowed role -> 403 Forbidden (HTML or JSON).
    """
    normalized_allowed = tuple(r.lower() for r in allowed_roles)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if user is None:
                log_error(401, request.method, request.path, "[guest] Authentication required")
                if request.path.startswith("/api/"):
                    return jsonify({
                        "status": "error",
                        "code": 401,
                        "reason": "Authentication required. Please log in.",
                        "role": "guest",
                        "path": request.path,
                    }), 401
                return redirect(url_for("auth.login_form", next=request.path))

            user_role = (user.role or "student").strip().lower()
            if user_role not in normalized_allowed:
                allowed_str = ", ".join(r.capitalize() for r in normalized_allowed)
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


def _check_central_rbac(path: str, method: str, role: str):
    """
    Central request-level RBAC check enforcing ddd.md role matrix on web routes.
    Returns None if permitted, or a redirect / abort(403) if blocked.
    """
    clean_path = path.rstrip("/") or "/"

    # 1. Public exact routes & prefixes
    if clean_path in PUBLIC_EXACT_PATHS or any(path.startswith(p) for p in PUBLIC_PREFIXES):
        return None

    # 2. API routes remain accessible for programmatic/Swagger testing unless X-User-Id is provided
    if path.startswith("/api/"):
        if role != "guest":
            # Enforce RBAC on write operations when an authenticated API user is active
            if path.startswith("/api/job-postings") and not path.endswith("/applications") and method in ("POST", "PUT", "PATCH", "DELETE"):
                if role not in ("alumni", "academician", "admin"):
                    abort(403, description=f"Role '{role}' cannot create, update, or delete job postings.")
            elif path.startswith("/api/announcements") and method in ("POST", "PUT", "PATCH", "DELETE"):
                if role not in ("alumni", "academician", "admin"):
                    abort(403, description=f"Role '{role}' cannot create, update, or delete announcements.")
        return None

    # 3. Web read-only views allowed for guests per ddd.md (/, /announcements, /job-postings)
    if method == "GET" and clean_path in ("/announcements", "/job-postings"):
        return None

    # 4. All other web routes (/users, /applications, /admin, /new, /edit, /delete) require login
    if role == "guest":
        log_error(401, method, path, "[guest] Unauthenticated access to protected route -> redirect /login")
        return redirect(url_for("auth.login_form", next=path))

    # 5. Authenticated self-service & read-only views allowed for all logged-in roles
    parts = [p for p in clean_path.split("/") if p]
    if clean_path in ("/settings", "/settings/delete"):
        return None
    if method == "GET" and clean_path in ("/users", "/applications"):
        return None
    if method == "GET" and len(parts) == 2 and parts[0] == "users" and parts[1].isdigit():
        return None

    # 5. Role-specific restrictions per ddd.md
    if clean_path.startswith("/admin"):
        if role != "admin":
            abort(
                403,
                description=f"Your current role is '{role.capitalize()}'. The Admin Panel (/admin) is restricted to Admin users only.",
            )

    elif clean_path.startswith("/job-postings"):
        if role not in ("alumni", "academician", "admin"):
            abort(
                403,
                description=f"Your current role is '{role.capitalize()}'. Only Alumni, Academician, and Admin can manage job postings.",
            )

    elif clean_path.startswith("/announcements"):
        if role not in ("alumni", "academician", "admin"):
            abort(
                403,
                description=f"Your current role is '{role.capitalize()}'. Only Alumni, Academician, and Admin can publish or manage announcements.",
            )

    elif clean_path.startswith("/applications"):
        if clean_path in ("/applications", "/applications/new"):
            if role not in ("student", "alumni", "admin"):
                abort(
                    403,
                    description=f"Your current role is '{role.capitalize()}'. Only Students, Alumni, and Admin can submit job applications.",
                )
        else:
            # /applications/<id>/edit or /delete
            if role not in ("alumni", "academician", "admin"):
                abort(
                    403,
                    description=f"Your current role is '{role.capitalize()}'. Reviewing, editing, or deleting applications is restricted to Alumni, Academician, and Admin.",
                )

    return None


def init_auth_middleware(app: Flask) -> None:
    """Register the Auth & RBAC Middleware hooks and error handlers on the Flask app."""

    @app.before_request
    def _authenticate_and_authorize():
        g.current_user = get_current_user()
        g.current_role = (
            (g.current_user.role or "student").strip().lower()
            if g.current_user is not None
            else "guest"
        )
        return _check_central_rbac(request.path, request.method, g.current_role)

    @app.after_request
    def _attach_auth_headers(response):
        response.headers["X-Auth-Role"] = getattr(g, "current_role", "guest")
        if getattr(g, "current_user", None) is not None:
            response.headers["X-Auth-User"] = str(g.current_user.id)
        return response

    @app.context_processor
    def _inject_auth_context():
        user_id = session.get("user_id")
        user = User.get_by_id(int(user_id)) if user_id else None
        role = (user.role or "student").strip().lower() if user is not None else "guest"
        return {
            "current_user": user,
            "current_role": role,
            "is_admin": is_admin(user),
        }

    @app.errorhandler(401)
    def _handle_401(error: Unauthorized):
        reason = (
            error.description
            if error and error.description
            else "Authentication is required to access this resource."
        )
        log_error(401, request.method, request.path, f"[guest] {reason}")
        if request.path.startswith("/api/"):
            return jsonify({
                "status": "error",
                "code": 401,
                "reason": reason,
                "role": "guest",
                "method": request.method,
                "path": request.path,
            }), 401
        return redirect(url_for("auth.login_form", next=request.path))

    @app.errorhandler(403)
    def _handle_403(error: Forbidden):
        user_role = get_current_role()
        reason = (
            error.description
            if error and error.description
            else "You do not have permission to perform this action."
        )
        log_error(403, request.method, request.path, f"[{user_role}] {reason}")
        if request.path.startswith("/api/"):
            return jsonify({
                "status": "error",
                "code": 403,
                "reason": reason,
                "role": user_role,
                "method": request.method,
                "path": request.path,
            }), 403
        return (
            render_template(
                "403.html",
                reason=reason,
                requested_path=request.path,
                user_role=user_role,
            ),
            403,
        )
