"""
JobPosting web routes — HTML responses.
Blueprint prefix: /job-postings
Delegates to: JobPostingController
RBAC (ddd.md):
  - View list (GET /job-postings): All roles (including guest)
  - Create / Edit / Delete: Restricted to alumni, academician, admin (students & guests forbidden)
"""

from flask import Blueprint, abort, render_template, request, redirect, url_for
from app.controllers.job_posting_controller import JobPostingController
from app.middleware.auth_guardian import require_roles

job_postings_bp = Blueprint("job_postings", __name__, url_prefix="/job-postings")


@job_postings_bp.route("/", methods=["GET"], strict_slashes=False)
@job_postings_bp.route("", methods=["GET"])
def index():
    result = JobPostingController.index()
    return render_template("job_posting/index.html", job_postings=result["job_postings"])


@job_postings_bp.route("/new", methods=["GET"])
@require_roles("alumni", "academician", "admin")
def new():
    return render_template("job_posting/create.html", error=None)


@job_postings_bp.route("/", methods=["POST"], strict_slashes=False)
@job_postings_bp.route("", methods=["POST"])
@require_roles("alumni", "academician", "admin")
def create():
    data = request.form.to_dict()
    result = JobPostingController.create(data)
    if not result["success"]:
        return render_template("job_posting/create.html", error=result["error"]), 400
    return redirect(url_for("job_postings.index"))


@job_postings_bp.route("/<int:job_posting_id>/edit", methods=["GET"])
@require_roles("alumni", "academician", "admin")
def edit(job_posting_id):
    result = JobPostingController.show(job_posting_id)
    if not result["success"]:
        abort(404, description=result["error"])
    return render_template("job_posting/edit.html", job_posting=result["job_posting"], error=None)


@job_postings_bp.route("/<int:job_posting_id>/edit", methods=["POST"])
@require_roles("alumni", "academician", "admin")
def update(job_posting_id):
    data = request.form.to_dict()
    result = JobPostingController.update(job_posting_id, data)
    if not result["success"]:
        status = 404 if "not found" in result["error"] else 400
        if status == 400:
            jp_result = JobPostingController.show(job_posting_id)
            jp_data = jp_result["job_posting"] if jp_result["success"] else data
            return render_template("job_posting/edit.html", job_posting=jp_data, error=result["error"]), 400
        abort(404, description=result["error"])
    return redirect(url_for("job_postings.index"))


@job_postings_bp.route("/<int:job_posting_id>/delete", methods=["POST"])
@require_roles("alumni", "academician", "admin")
def delete(job_posting_id):
    result = JobPostingController.delete(job_posting_id)
    if not result["success"]:
        abort(404, description=result["message"])
    return redirect(url_for("job_postings.index"))
