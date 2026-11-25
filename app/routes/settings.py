"""
Account Settings routes — self-service profile, career, security, and account deletion.
Routes:
  - GET  /settings        — Render settings.html for current_user (guest -> /login)
  - POST /settings        — Update profile/career or email/password (role is read-only)
  - POST /settings/delete — Permanently delete current_user's account, session.clear(), redirect /
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app.controllers.user_controller import UserController
from app.middleware.auth_middleware import get_current_user, login_required

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET"])
@login_required
def settings_page():
    """Render the authenticated user's settings page."""
    return render_template("settings.html")


@settings_bp.route("/settings", methods=["POST"])
@login_required
def settings_update():
    """Handle Profile & Career or Email & Password updates for current_user."""
    user = get_current_user()
    data = request.form.to_dict()
    form_type = (data.get("form_type") or "profile").strip().lower()

    if form_type == "security":
        result = UserController.update_security_settings(user.id, data)
    else:
        result = UserController.update_profile_settings(user.id, data)

    if result["success"]:
        flash(result["message"], "success")
    else:
        flash(result["error"], "error")

    return redirect(url_for("settings.settings_page"))


@settings_bp.route("/settings/delete", methods=["POST"])
@login_required
def settings_delete_account():
    """Permanently delete the authenticated user's own account and clear session."""
    user = get_current_user()
    result = UserController.delete_own_account(user.id)

    if not result["success"]:
        flash(result["error"], "error")
        return redirect(url_for("settings.settings_page"))

    session.clear()
    flash(result["message"], "success")
    return redirect(url_for("index"))
