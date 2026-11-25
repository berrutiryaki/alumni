"""
Admin Panel routes — unified dashboard and data manipulation for system administrators.
Blueprint prefix: /admin
Restricted to: admin role (@require_roles("admin"))
"""

import os
from flask import Blueprint, abort, redirect, render_template, request, url_for
from app.database import db
from app.middleware.auth_middleware import require_roles
from app.middleware.error_log import LOG_FILE
from app.models.user import User, VALID_ROLES
from app.models.announcement import Announcement
from app.models.job_posting import JobPosting
from app.models.application import Application

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _read_recent_logs(limit: int = 25) -> list[str]:
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
            lines = [line.rstrip() for line in f if line.strip()]
        return lines[-limit:][::-1]
    except Exception:
        return []


@admin_bp.route("/", methods=["GET"], strict_slashes=False)
@admin_bp.route("", methods=["GET"])
@require_roles("admin")
def dashboard():
    """Render the unified Admin Panel dashboard."""
    users = User.get_all()
    job_postings = JobPosting.get_all()
    applications = Application.get_all()
    announcements = Announcement.get_all()

    stats = {
        "users_total": len(users),
        "students": sum(1 for u in users if (u.get("role") or u.get("status")) == "student"),
        "alumni": sum(1 for u in users if (u.get("role") or u.get("status")) == "alumni"),
        "academicians": sum(1 for u in users if (u.get("role") or u.get("status")) == "academician"),
        "admins": sum(1 for u in users if (u.get("role") or u.get("status")) == "admin"),
        "jobs_total": len(job_postings),
        "jobs_active": sum(1 for j in job_postings if j.get("is_active")),
        "apps_total": len(applications),
        "apps_pending": sum(1 for a in applications if a.get("status") == "pending"),
        "apps_reviewed": sum(1 for a in applications if a.get("status") == "reviewed"),
        "apps_accepted": sum(1 for a in applications if a.get("status") == "accepted"),
        "apps_rejected": sum(1 for a in applications if a.get("status") == "rejected"),
        "ann_total": len(announcements),
        "ann_active": sum(1 for a in announcements if a.get("is_active")),
    }

    active_tab = request.args.get("tab", "users")
    notice = request.args.get("msg")

    return render_template(
        "admin/index.html",
        stats=stats,
        users=users,
        job_postings=job_postings,
        applications=applications,
        announcements=announcements,
        recent_logs=_read_recent_logs(25),
        active_tab=active_tab,
        notice=notice,
    )


# ------------------------------------------------------------------
# User Manipulation Endpoints
# ------------------------------------------------------------------

@admin_bp.route("/users/<int:user_id>/role", methods=["POST"])
@require_roles("admin")
def change_user_role(user_id: int):
    user = User.get_by_id(user_id)
    if user is None:
        abort(404, description=f"User {user_id} not found")
    new_role = (request.form.get("role") or "").strip().lower()
    if new_role not in VALID_ROLES:
        abort(400, description=f"Invalid role '{new_role}'")

    User.partial_update(user_id, {"role": new_role, "status": new_role})
    return redirect(url_for("admin.dashboard", tab="users", msg=f"Updated {user.name} (#{user.id}) role to '{new_role}'."))


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@require_roles("admin")
def delete_user(user_id: int):
    user = User.get_by_id(user_id)
    if user is None:
        abort(404, description=f"User {user_id} not found")
    name = user.name
    # Remove dependent applications first so FK doesn't block deletion
    Application.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    User.delete(user_id)
    return redirect(url_for("admin.dashboard", tab="users", msg=f"Deleted user '{name}' (#{user_id})."))


# ------------------------------------------------------------------
# Job Posting Manipulation Endpoints
# ------------------------------------------------------------------

@admin_bp.route("/job-postings/<int:job_id>/toggle", methods=["POST"])
@require_roles("admin")
def toggle_job_posting(job_id: int):
    jp = JobPosting.get_by_id(job_id)
    if jp is None:
        abort(404, description=f"Job posting {job_id} not found")
    new_state = not bool(jp.is_active)
    JobPosting.partial_update(job_id, {"is_active": new_state})
    state_label = "Active" if new_state else "Closed"
    return redirect(url_for("admin.dashboard", tab="jobs", msg=f"Job #{job_id} ({jp.title}) set to {state_label}."))


@admin_bp.route("/job-postings/<int:job_id>/delete", methods=["POST"])
@require_roles("admin")
def delete_job_posting(job_id: int):
    jp = JobPosting.get_by_id(job_id)
    if jp is None:
        abort(404, description=f"Job posting {job_id} not found")
    title = jp.title
    Application.query.filter_by(job_posting_id=job_id).delete()
    db.session.commit()
    JobPosting.delete(job_id)
    return redirect(url_for("admin.dashboard", tab="jobs", msg=f"Deleted job posting '{title}' (#{job_id})."))


# ------------------------------------------------------------------
# Application Manipulation Endpoints
# ------------------------------------------------------------------

@admin_bp.route("/applications/<int:app_id>/status", methods=["POST"])
@require_roles("admin")
def change_application_status(app_id: int):
    app_rec = Application.get_by_id(app_id)
    if app_rec is None:
        abort(404, description=f"Application {app_id} not found")
    new_status = (request.form.get("status") or "pending").strip().lower()
    if new_status not in ("pending", "reviewed", "accepted", "rejected"):
        abort(400, description=f"Invalid application status '{new_status}'")
    Application.partial_update(app_id, {"status": new_status})
    return redirect(url_for("admin.dashboard", tab="applications", msg=f"Application #{app_id} status updated to '{new_status}'."))


@admin_bp.route("/applications/<int:app_id>/delete", methods=["POST"])
@require_roles("admin")
def delete_application(app_id: int):
    deleted = Application.delete(app_id)
    if not deleted:
        abort(404, description=f"Application {app_id} not found")
    return redirect(url_for("admin.dashboard", tab="applications", msg=f"Deleted application #{app_id}."))


# ------------------------------------------------------------------
# Announcement Manipulation Endpoints
# ------------------------------------------------------------------

@admin_bp.route("/announcements/<int:ann_id>/toggle", methods=["POST"])
@require_roles("admin")
def toggle_announcement(ann_id: int):
    ann = Announcement.get_by_id(ann_id)
    if ann is None:
        abort(404, description=f"Announcement {ann_id} not found")
    new_state = not bool(ann.is_active)
    Announcement.partial_update(ann_id, {"is_active": new_state})
    state_label = "Active" if new_state else "Inactive"
    return redirect(url_for("admin.dashboard", tab="announcements", msg=f"Announcement #{ann_id} ({ann.title}) set to {state_label}."))


@admin_bp.route("/announcements/<int:ann_id>/delete", methods=["POST"])
@require_roles("admin")
def delete_announcement(ann_id: int):
    ann = Announcement.get_by_id(ann_id)
    if ann is None:
        abort(404, description=f"Announcement {ann_id} not found")
    title = ann.title
    Announcement.delete(ann_id)
    return redirect(url_for("admin.dashboard", tab="announcements", msg=f"Deleted announcement '{title}' (#{ann_id})."))
