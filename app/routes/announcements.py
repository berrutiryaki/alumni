"""
Announcement web routes — HTML responses.
Blueprint prefix: /announcements
Delegates to: AnnouncementController
RBAC (ddd.md):
  - View list (GET /announcements): All roles (including guest)
  - Create / Edit / Delete: Restricted to alumni, academician, admin (students & guests forbidden)
"""

from flask import Blueprint, abort, render_template, request, redirect, url_for
from app.controllers.announcement_controller import AnnouncementController
from app.middleware.auth_guardian import require_roles

announcements_bp = Blueprint("announcements", __name__, url_prefix="/announcements")


@announcements_bp.route("/", methods=["GET"], strict_slashes=False)
@announcements_bp.route("", methods=["GET"])
def index():
    result = AnnouncementController.index()
    return render_template("announcement/index.html", announcements=result["announcements"])


@announcements_bp.route("/new", methods=["GET"])
@require_roles("alumni", "academician", "admin")
def new():
    return render_template("announcement/create.html", error=None)


@announcements_bp.route("/", methods=["POST"], strict_slashes=False)
@announcements_bp.route("", methods=["POST"])
@require_roles("alumni", "academician", "admin")
def create():
    data = request.form.to_dict()
    result = AnnouncementController.create(data)
    if not result["success"]:
        return render_template("announcement/create.html", error=result["error"]), 400
    return redirect(url_for("announcements.index"))


@announcements_bp.route("/<int:announcement_id>/edit", methods=["GET"])
@require_roles("alumni", "academician", "admin")
def edit(announcement_id):
    result = AnnouncementController.show(announcement_id)
    if not result["success"]:
        abort(404, description=result["error"])
    return render_template("announcement/edit.html", announcement=result["announcement"], error=None)


@announcements_bp.route("/<int:announcement_id>/edit", methods=["POST"])
@require_roles("alumni", "academician", "admin")
def update(announcement_id):
    data = request.form.to_dict()
    result = AnnouncementController.update(announcement_id, data)
    if not result["success"]:
        status = 404 if "not found" in result["error"] else 400
        if status == 400:
            ann_result = AnnouncementController.show(announcement_id)
            ann_data = ann_result["announcement"] if ann_result["success"] else data
            return render_template("announcement/edit.html", announcement=ann_data, error=result["error"]), 400
        abort(404, description=result["error"])
    return redirect(url_for("announcements.index"))


@announcements_bp.route("/<int:announcement_id>/delete", methods=["POST"])
@require_roles("alumni", "academician", "admin")
def delete(announcement_id):
    result = AnnouncementController.delete(announcement_id)
    if not result["success"]:
        abort(404, description=result["message"])
    return redirect(url_for("announcements.index"))
