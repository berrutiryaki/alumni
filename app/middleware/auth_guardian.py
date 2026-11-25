"""
Backwards-compatible re-exports from app.middleware.auth_middleware.
"""

from app.middleware.auth_middleware import (
    get_current_role,
    get_current_user,
    init_auth_middleware as init_forbidden_guardian,
    init_auth_middleware,
    login_required,
    require_roles,
)

__all__ = [
    "init_auth_middleware",
    "init_forbidden_guardian",
    "login_required",
    "require_roles",
    "get_current_user",
    "get_current_role",
]
