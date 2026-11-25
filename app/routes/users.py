"""
User web routes — HTML responses.
Blueprint prefix: /users
Delegates to: UserController
RBAC (ddd.md):
  - View list & profile (GET /users, GET /users/<id>): All roles
  - Edit profile (GET/POST /users/<id>/edit): Own profile (current_user.id == user_id) or admin
  - Direct create / delete in directory: Restricted to admin (other users register via /register)
"""

from flask import Blueprint, abort, render_template, request, redirect, url_for
from app.controllers.user_controller import UserController
from app.middleware.auth_guardian import get_current_user, login_required, require_roles

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["GET"], strict_slashes=False)
@users_bp.route("", methods=["GET"])
@login_required
def index():
    """List all users (HTML) — requires authenticated user."""
    result = UserController.index()
    return render_template("user/index.html", users=result["users"])


@users_bp.route("/new", methods=["GET"])
@require_roles("admin")
def new():
    """Show the form to create a new user (Admin only)."""
    return render_template("user/create.html", error=None)


@users_bp.route("/", methods=["POST"], strict_slashes=False)
@users_bp.route("", methods=["POST"])
@require_roles("admin")
def create():
    """Process the form submission and create a new user (Admin only)."""
    data = request.form.to_dict()
    result = UserController.create(data)

    if not result["success"]:
        return render_template("user/create.html", error=result["error"]), 400

    return redirect(url_for("users.index"))


@users_bp.route("/<int:user_id>", methods=["GET"])
@login_required
def show(user_id):
    """Show the profile page for a single user — requires authenticated user."""
    result = UserController.show(user_id)
    if not result["success"]:
        abort(404, description=result["error"])
    return render_template("user/show.html", user=result["user"])


def _ensure_self_or_admin(target_user_id: int):
    current = get_current_user()
    if current is None:
        return redirect(url_for("auth.login_form"))
    if not current.is_admin and current.id != target_user_id:
        abort(
            403,
            description="You can only edit your own profile. Editing other members' profiles requires the Admin role.",
        )
    return None


@users_bp.route("/<int:user_id>/edit", methods=["GET"])
def edit(user_id):
    """Show the form to edit an existing user (self or admin)."""
    guard = _ensure_self_or_admin(user_id)
    if guard is not None:
        return guard
    result = UserController.show(user_id)
    if not result["success"]:
        abort(404, description=result["error"])
    return render_template("user/edit.html", user=result["user"], error=None)


@users_bp.route("/<int:user_id>/edit", methods=["POST"])
def update(user_id):
    """Process the edit form submission (self or admin)."""
    guard = _ensure_self_or_admin(user_id)
    if guard is not None:
        return guard
    data = request.form.to_dict()
    current = get_current_user()
    # Prevent non-admin users from escalating their own role
    if current is not None and not current.is_admin:
        data["role"] = current.role
        data["status"] = current.role
    result = UserController.update(user_id, data)

    if not result["success"]:
        status = 404 if "not found" in result["error"] else 400
        if status == 400:
            user_result = UserController.show(user_id)
            user_data = user_result["user"] if user_result["success"] else data
            return render_template("user/edit.html", user=user_data, error=result["error"]), 400
        abort(404, description=result["error"])

    return redirect(url_for("users.index"))


@users_bp.route("/<int:user_id>/delete", methods=["POST"])
@require_roles("admin")
def delete(user_id):
    """Process the delete form submission (Admin only)."""
    result = UserController.delete(user_id)
    if not result["success"]:
        abort(404, description=result["message"])
    return redirect(url_for("users.index"))
