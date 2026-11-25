from app.middleware.logger import init_logger
from app.middleware.not_found_guardian import init_not_found_guardian
from app.middleware.server_error_guardian import init_server_error_guardian
from app.middleware.auth_middleware import (
    init_auth_middleware,
    login_required,
    require_roles,
    get_current_user,
    get_current_role,
)

__all__ = [
    "init_logger",
    "init_not_found_guardian",
    "init_server_error_guardian",
    "init_auth_middleware",
    "login_required",
    "require_roles",
    "get_current_user",
    "get_current_role",
]
