"""
Application web routes — HTML responses.
Blueprint prefix: /applications
Delegates to: ApplicationController
RBAC (ddd.md):
  - View list (GET /applications): All roles
  - Submit application (GET /applications/new, POST /applications): Restricted to student, alumni, admin
  - Review / Edit / Delete application: Restricted to alumni, academician, admin
"""

from flask import Blueprint, abort, render_template, request, redirect, url_for
from app.controllers.application_controller import ApplicationController
from app.middleware.auth_guardian import require_roles
from app.models.user import User
from app.models.job_posting import JobPosting

applications_bp = Blueprint("applications", __name__, url_prefix="/applications")


@applications_bp.route("/", methods=["GET"], strict_slashes=False)
@applications_bp.route("", methods=["GET"])
def index():
    result = ApplicationController.index()
    return render_template("application/index.html", applications=result["applications"])


@applications_bp.route("/new", methods=["GET"])
@require_roles("student", "alumni", "admin")
def new():
    users = User.query.order_by(User.name.asc()).all()
    job_postings = JobPosting.query.order_by(JobPosting.title.asc()).all()
    return render_template("application/create.html", users=users, job_postings=job_postings, error=None)


@applications_bp.route("/", methods=["POST"], strict_slashes=False)
@applications_bp.route("", methods=["POST"])
@require_roles("student", "alumni", "admin")
def create():
    data = request.form.to_dict()
    result = ApplicationController.create(data)
    if not result["success"]:
        users = User.query.order_by(User.name.asc()).all()
        job_postings = JobPosting.query.order_by(JobPosting.title.asc()).all()
        return render_template("application/create.html", users=users, job_postings=job_postings, error=result["error"]), 400
    return redirect(url_for("applications.index"))


@applications_bp.route("/<int:application_id>/edit", methods=["GET"])
@require_roles("alumni", "academician", "admin")
def edit(application_id):
    result = ApplicationController.show(application_id)
    if not result["success"]:
        abort(404, description=result["error"])
    users = User.query.order_by(User.name.asc()).all()
    job_postings = JobPosting.query.order_by(JobPosting.title.asc()).all()
    return render_template("application/edit.html", application=result["application"], users=users, job_postings=job_postings, error=None)


@applications_bp.route("/<int:application_id>/edit", methods=["POST"])
@require_roles("alumni", "academician", "admin")
def update(application_id):
    data = request.form.to_dict()
    result = ApplicationController.update(application_id, data)
    if not result["success"]:
        status = 404 if "not found" in result["error"].lower() else 400
        if status == 400:
            app_result = ApplicationController.show(application_id)
            app_data = app_result["application"] if app_result["success"] else data
            users = User.query.order_by(User.name.asc()).all()
            job_postings = JobPosting.query.order_by(JobPosting.title.asc()).all()
            return render_template("application/edit.html", application=app_data, users=users, job_postings=job_postings, error=result["error"]), 400
        abort(404, description=result["error"])
    return redirect(url_for("applications.index"))


@applications_bp.route("/<int:application_id>/delete", methods=["POST"])
@require_roles("alumni", "academician", "admin")
def delete(application_id):
    result = ApplicationController.delete(application_id)
    if not result["success"]:
        abort(404, description=result["message"])
    return redirect(url_for("applications.index"))
