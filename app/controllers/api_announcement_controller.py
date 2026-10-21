"""
ApiAnnouncementController — JSON API controller with database connection.

Handles /api/announcements routes and returns structured JSON responses.
Delegates all data operations to the SQLAlchemy Announcement model.
"""

from flask import request, jsonify
from app.models.announcement import Announcement


class ApiAnnouncementController:

    @staticmethod
    def index():
        try:
            return jsonify({
                "status": "success",
                "count": Announcement.query.count(),
                "announcements": Announcement.get_all()
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def show(announcement_id: int):
        try:
            announcement = Announcement.get_by_id(announcement_id)
            if announcement is None:
                return jsonify({"status": "error", "message": f"Announcement {announcement_id} not found"}), 404
            return jsonify({"status": "success", "announcement": announcement.to_dict()}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def create(extra_data: dict = None):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        if extra_data:
            data.update(extra_data)

        title = (data.get("title") or "").strip()
        content = (data.get("content") or "").strip()

        if not title or not content:
            return jsonify({"status": "error", "message": "title and content are required"}), 400

        try:
            announcement = Announcement.create({
                "title": title,
                "content": content,
                "author": (data.get("author") or "").strip() or None,
                "is_active": data.get("is_active", True) not in [False, "false", "0", 0],
                "user_id": data.get("user_id"),
            })
            return jsonify({"status": "success", "announcement": announcement.to_dict()}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def update(announcement_id: int):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        title = (data.get("title") or "").strip()
        content = (data.get("content") or "").strip()

        if not title or not content:
            return jsonify({"status": "error", "message": "title and content are required"}), 400

        try:
            announcement = Announcement.update(announcement_id, {
                "title": title,
                "content": content,
                "author": (data.get("author") or "").strip() or None,
                "is_active": data.get("is_active", True) not in [False, "false", "0", 0],
            })
            if announcement is None:
                return jsonify({"status": "error", "message": f"Announcement {announcement_id} not found"}), 404
            return jsonify({"status": "success", "announcement": announcement.to_dict()}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def partial_update(announcement_id: int):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        try:
            announcement = Announcement.partial_update(announcement_id, data)
            if announcement is None:
                return jsonify({"status": "error", "message": f"Announcement {announcement_id} not found"}), 404
            return jsonify({"status": "success", "announcement": announcement.to_dict()}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def delete(announcement_id: int):
        try:
            deleted = Announcement.delete(announcement_id)
            if not deleted:
                return jsonify({"status": "error", "message": f"Announcement {announcement_id} not found"}), 404
            return jsonify({"status": "success", "message": f"Announcement {announcement_id} deleted"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    # ------------------------------------------------------------------
    # Nested: filter by user_id
    # ------------------------------------------------------------------

    @staticmethod
    def index_by_user(user_id: int):
        """Return all announcements authored by a specific user."""
        try:
            from app.models.user import User
            user = User.get_by_id(user_id)
            if user is None:
                return jsonify({"status": "error", "message": f"User {user_id} not found"}), 404
            announcements = Announcement.query.filter_by(user_id=user_id).order_by(Announcement.id.asc()).all()
            return jsonify({
                "status": "success",
                "count": len(announcements),
                "user_id": user_id,
                "announcements": [a.to_dict() for a in announcements]
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
