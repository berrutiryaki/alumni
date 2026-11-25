"""
Application web routes — HTML responses.
Blueprint prefix: /applications
Delegates to: ApplicationController
RBAC & Privacy Rules (ddd.md):
  - GET /applications: Authenticated only (guest -> /login), privacy-filtered:
      * admin -> all applications
      * job posting owner (posted_by matches current_user.name or email) -> applications for their postings
      * student / alumni -> own submitted applications (user_id == current_user.id)
  - GET /applications/new (?job_posting_id=<id>) & GET /applications/new/<id>:
      * Restricted to student, alumni, admin
      * Redirects to /job-postings if no valid job posting is selected
  - POST /applications:
      * Restricted to student, alumni, admin
      * Strictly binds user_id = current_user.id and status = 'pending'
      * Prevents duplicate (user_id, job_posting_id) with 409 Conflict
  - POST /applications/<id>/status, GET/POST /applications/<id>/edit, POST /applications/<id>/delete:
      * Restricted strictly to admin OR the owner of the target job posting (403 Forbidden otherwise)
"""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from app.controllers.application_controller import ApplicationController
from app.middleware.auth_middleware import get_current_user, login_required, require_roles
from app.models.application import Application
from app.models.job_posting import JobPosting

applications_bp = Blueprint("applications", __name__, url_prefix="/applications")


def _resolve_job_posting(raw_job_id) -> JobPosting | None:
    """Safely parse job_posting_id and return the JobPosting record or None."""
    if raw_job_id is None or str(raw_job_id).strip() == "":
        return None
    try:
        return JobPosting.get_by_id(int(raw_job_id))
    except (TypeError, ValueError):
        return None


@applications_bp.route("/", methods=["GET"], strict_slashes=False)
@applications_bp.route("", methods=["GET"])
@login_required
def index():
    current_user = get_current_user()
    result = ApplicationController.index_for_user(current_user)
    return render_template("application/index.html", applications=result["applications"])


@applications_bp.route("/new", methods=["GET"])
@applications_bp.route("/new/<int:job_posting_id>", methods=["GET"])
@require_roles("student", "alumni", "admin")
def new(job_posting_id=None):
    raw_id = job_posting_id if job_posting_id is not None else request.args.get("job_posting_id")
    job = _resolve_job_posting(raw_id)
    if job is None:
        flash("Please select an open job posting before applying.", "error")
        return redirect(url_for("job_postings.index"))

    current_user = get_current_user()
    already_applied = Application.find_duplicate(current_user.id, job.id) is not None
    error = (
        f"You have already submitted an application for '{job.title}' at {job.company}."
        if already_applied
        else None
    )
    return render_template(
        "application/create.html",
        job=job,
        error=error,
        already_applied=already_applied,
        form_data={},
    )


@applications_bp.route("/", methods=["POST"], strict_slashes=False)
@applications_bp.route("", methods=["POST"])
@applications_bp.route("/new/<int:job_posting_id>", methods=["POST"])
@require_roles("student", "alumni", "admin")
def create(job_posting_id=None):
    current_user = get_current_user()
    data = request.form.to_dict()
    raw_id = (
        job_posting_id
        if job_posting_id is not None
        else (data.get("job_posting_id") or request.args.get("job_posting_id"))
    )
    job = _resolve_job_posting(raw_id)
    if job is None:
        flash("Please select a valid job posting before applying.", "error")
        return redirect(url_for("job_postings.index"))

    # Never accept user_id or status from client form; bind strictly in backend
    payload = {
        "job_posting_id": job.id,
        "resume_url": data.get("resume_url"),
        "cover_letter": data.get("cover_letter"),
    }
    result = ApplicationController.create(payload, current_user=current_user)
    if not result["success"]:
        status_code = result.get("status_code", 400)
        return (
            render_template(
                "application/create.html",
                job=job,
                error=result["error"],
                already_applied=(status_code == 409),
                form_data=data,
            ),
            status_code,
        )

    flash(f"Your application for '{job.title}' at {job.company} has been submitted (Status: Pending).", "success")
    return redirect(url_for("applications.index"))


@applications_bp.route("/<int:application_id>/status", methods=["POST"])
@login_required
def update_status(application_id):
    current_user = get_current_user()
    new_status = request.form.get("status", "")
    result = ApplicationController.update_status(application_id, new_status, current_user)

    if not result["success"]:
        code = result.get("status_code", 400)
        if code == 403:
            abort(403, description=result["error"])
        if code == 404:
            abort(404, description=result["error"])
        flash(result["error"], "error")
        return redirect(url_for("applications.index"))

    flash(result["message"], "success")
    return redirect(url_for("applications.index"))


@applications_bp.route("/<int:application_id>/edit", methods=["GET"])
@login_required
def edit(application_id):
    current_user = get_current_user()
    app_rec = Application.get_by_id(application_id)
    if app_rec is None:
        abort(404, description=f"Application {application_id} not found")
    if not ApplicationController.can_manage_application(app_rec, current_user):
        abort(
            403,
            description="Only an administrator or the owner of this job posting can edit this application.",
        )
    return render_template("application/edit.html", application=app_rec.to_dict(), error=None)


@applications_bp.route("/<int:application_id>/edit", methods=["POST"])
@login_required
def update(application_id):
    current_user = get_current_user()
    data = request.form.to_dict()
    result = ApplicationController.update(application_id, data, current_user=current_user)
    if not result["success"]:
        code = result.get("status_code", 400)
        if code == 403:
            abort(403, description=result["error"])
        if code == 404:
            abort(404, description=result["error"])
        app_rec = Application.get_by_id(application_id)
        app_data = app_rec.to_dict() if app_rec else data
        return render_template("application/edit.html", application=app_data, error=result["error"]), 400

    flash(f"Application #{application_id} updated successfully.", "success")
    return redirect(url_for("applications.index"))


@applications_bp.route("/<int:application_id>/delete", methods=["POST"])
@login_required
def delete(application_id):
    current_user = get_current_user()
    result = ApplicationController.delete(application_id, current_user=current_user)
    if not result["success"]:
        code = result.get("status_code", 404)
        if code == 403:
            abort(403, description=result["message"])
        abort(404, description=result["message"])
    flash(result["message"], "success")
    return redirect(url_for("applications.index"))
