"""
Announcement web routes — HTML responses.
Blueprint prefix: /announcements
Delegates to: AnnouncementController
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.announcement_controller import AnnouncementController

announcements_bp = Blueprint("announcements", __name__, url_prefix="/announcements")


@announcements_bp.route("/", methods=["GET"])
def index():
    result = AnnouncementController.index()
    return render_template("announcement/index.html", announcements=result["announcements"])


@announcements_bp.route("/new", methods=["GET"])
def new():
    return render_template("announcement/create.html", error=None)


@announcements_bp.route("/", methods=["POST"])
def create():
    data = request.form.to_dict()
    result = AnnouncementController.create(data)
    if not result["success"]:
        return render_template("announcement/create.html", error=result["error"]), 400
    return redirect(url_for("announcements.index"))


@announcements_bp.route("/<int:announcement_id>/edit", methods=["GET"])
def edit(announcement_id):
    result = AnnouncementController.show(announcement_id)
    if not result["success"]:
        return f"<h2>404 — {result['error']}</h2>", 404
    return render_template("announcement/edit.html", announcement=result["announcement"], error=None)


@announcements_bp.route("/<int:announcement_id>/edit", methods=["POST"])
def update(announcement_id):
    data = request.form.to_dict()
    result = AnnouncementController.update(announcement_id, data)
    if not result["success"]:
        status = 404 if "not found" in result["error"] else 400
        if status == 400:
            ann_result = AnnouncementController.show(announcement_id)
            ann_data = ann_result["announcement"] if ann_result["success"] else data
            return render_template("announcement/edit.html", announcement=ann_data, error=result["error"]), 400
        return f"<h2>{status} — {result['error']}</h2>", status
    return redirect(url_for("announcements.index"))


@announcements_bp.route("/<int:announcement_id>/delete", methods=["POST"])
def delete(announcement_id):
    result = AnnouncementController.delete(announcement_id)
    if not result["success"]:
        return f"<h2>404 — {result['message']}</h2>", 404
    return redirect(url_for("announcements.index"))
