"""
JobPosting web routes — HTML responses.
Blueprint prefix: /job-postings
Delegates to: JobPostingController
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.job_posting_controller import JobPostingController

job_postings_bp = Blueprint("job_postings", __name__, url_prefix="/job-postings")


@job_postings_bp.route("/", methods=["GET"], strict_slashes=False)
@job_postings_bp.route("", methods=["GET"])
def index():
    result = JobPostingController.index()
    return render_template("job_posting/index.html", job_postings=result["job_postings"])


@job_postings_bp.route("/new", methods=["GET"])
def new():
    return render_template("job_posting/create.html", error=None)


@job_postings_bp.route("/", methods=["POST"], strict_slashes=False)
@job_postings_bp.route("", methods=["POST"])
def create():
    data = request.form.to_dict()
    result = JobPostingController.create(data)
    if not result["success"]:
        return render_template("job_posting/create.html", error=result["error"]), 400
    return redirect(url_for("job_postings.index"))


@job_postings_bp.route("/<int:job_posting_id>/edit", methods=["GET"])
def edit(job_posting_id):
    result = JobPostingController.show(job_posting_id)
    if not result["success"]:
        return f"<h2>404 — {result['error']}</h2>", 404
    return render_template("job_posting/edit.html", job_posting=result["job_posting"], error=None)


@job_postings_bp.route("/<int:job_posting_id>/edit", methods=["POST"])
def update(job_posting_id):
    data = request.form.to_dict()
    result = JobPostingController.update(job_posting_id, data)
    if not result["success"]:
        status = 404 if "not found" in result["error"] else 400
        if status == 400:
            jp_result = JobPostingController.show(job_posting_id)
            jp_data = jp_result["job_posting"] if jp_result["success"] else data
            return render_template("job_posting/edit.html", job_posting=jp_data, error=result["error"]), 400
        return f"<h2>{status} — {result['error']}</h2>", status
    return redirect(url_for("job_postings.index"))


@job_postings_bp.route("/<int:job_posting_id>/delete", methods=["POST"])
def delete(job_posting_id):
    result = JobPostingController.delete(job_posting_id)
    if not result["success"]:
        return f"<h2>404 — {result['message']}</h2>", 404
    return redirect(url_for("job_postings.index"))
