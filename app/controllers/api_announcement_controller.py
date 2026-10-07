"""
ApiAnnouncementController — JSON API controller.

Handles /api/announcements routes and returns structured JSON responses.
Delegates all data operations to the Announcement model.
"""

from flask import request, jsonify
from app.models.announcement import Announcement


class ApiAnnouncementController:

    @staticmethod
    def index():
        return jsonify({"status": "success", "announcements": Announcement.get_all()}), 200

    @staticmethod
    def show(announcement_id: int):
        announcement = Announcement.get_by_id(announcement_id)
        if announcement is None:
            return jsonify({"status": "error", "message": f"Announcement {announcement_id} not found"}), 404
        return jsonify({"status": "success", "announcement": announcement.to_dict()}), 200

    @staticmethod
    def create():
        data = request.form.to_dict() if request.form else request.get_json() or {}
        if not data.get("title") or not data.get("content"):
            return jsonify({"status": "error", "message": "title and content are required"}), 400
        announcement = Announcement.create(data)
        return jsonify({"status": "success", "announcement": announcement.to_dict()}), 201

    @staticmethod
    def update(announcement_id: int):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        if not data.get("title") or not data.get("content"):
            return jsonify({"status": "error", "message": "title and content are required"}), 400
        announcement = Announcement.update(announcement_id, data)
        if announcement is None:
            return jsonify({"status": "error", "message": f"Announcement {announcement_id} not found"}), 404
        return jsonify({"status": "success", "announcement": announcement.to_dict()}), 200

    @staticmethod
    def partial_update(announcement_id: int):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        announcement = Announcement.partial_update(announcement_id, data)
        if announcement is None:
            return jsonify({"status": "error", "message": f"Announcement {announcement_id} not found"}), 404
        return jsonify({"status": "success", "announcement": announcement.to_dict()}), 200

    @staticmethod
    def delete(announcement_id: int):
        deleted = Announcement.delete(announcement_id)
        if not deleted:
            return jsonify({"status": "error", "message": f"Announcement {announcement_id} not found"}), 404
        return jsonify({"status": "success", "message": f"Announcement {announcement_id} deleted"}), 200
