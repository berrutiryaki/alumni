"""
Application web routes — HTML responses.
Blueprint prefix: /applications
Delegates to: ApplicationController
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.application_controller import ApplicationController
from app.models.user import User
from app.models.job_posting import JobPosting

applications_bp = Blueprint("applications", __name__, url_prefix="/applications")


@applications_bp.route("/", methods=["GET"], strict_slashes=False)
@applications_bp.route("", methods=["GET"])
def index():
    result = ApplicationController.index()
    return render_template("application/index.html", applications=result["applications"])


@applications_bp.route("/new", methods=["GET"])
def new():
    users = User.query.order_by(User.name.asc()).all()
    job_postings = JobPosting.query.order_by(JobPosting.title.asc()).all()
    return render_template("application/create.html", users=users, job_postings=job_postings, error=None)


@applications_bp.route("/", methods=["POST"], strict_slashes=False)
@applications_bp.route("", methods=["POST"])
def create():
    data = request.form.to_dict()
    result = ApplicationController.create(data)
    if not result["success"]:
        users = User.query.order_by(User.name.asc()).all()
        job_postings = JobPosting.query.order_by(JobPosting.title.asc()).all()
        return render_template("application/create.html", users=users, job_postings=job_postings, error=result["error"]), 400
    return redirect(url_for("applications.index"))


@applications_bp.route("/<int:application_id>/edit", methods=["GET"])
def edit(application_id):
    result = ApplicationController.show(application_id)
    if not result["success"]:
        return f"<h2>404 — {result['error']}</h2>", 404
    users = User.query.order_by(User.name.asc()).all()
    job_postings = JobPosting.query.order_by(JobPosting.title.asc()).all()
    return render_template("application/edit.html", application=result["application"], users=users, job_postings=job_postings, error=None)


@applications_bp.route("/<int:application_id>/edit", methods=["POST"])
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
        return f"<h2>{status} — {result['error']}</h2>", status
    return redirect(url_for("applications.index"))


@applications_bp.route("/<int:application_id>/delete", methods=["POST"])
def delete(application_id):
    result = ApplicationController.delete(application_id)
    if not result["success"]:
        return f"<h2>404 — {result['message']}</h2>", 404
    return redirect(url_for("applications.index"))
