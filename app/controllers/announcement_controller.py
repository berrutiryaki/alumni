"""
AnnouncementController — HTML / web-facing controller.

Delegates all data operations to the Announcement model.
Returns plain dicts consumed by the web route layer.
"""

from app.models.announcement import Announcement


class AnnouncementController:

    @staticmethod
    def index() -> dict:
        return {"success": True, "announcements": Announcement.get_all()}

    @staticmethod
    def show(announcement_id: int) -> dict:
        announcement = Announcement.get_by_id(announcement_id)
        if announcement is None:
            return {"success": False, "announcement": None, "error": f"Announcement {announcement_id} not found"}
        return {"success": True, "announcement": announcement.to_dict(), "error": None}

    @staticmethod
    def create(data: dict) -> dict:
        if not data.get("title") or not data.get("content"):
            return {"success": False, "announcement": None, "error": "title and content are required"}
        announcement = Announcement.create(data)
        return {"success": True, "announcement": announcement.to_dict(), "error": None}

    @staticmethod
    def update(announcement_id: int, data: dict) -> dict:
        if not data.get("title") or not data.get("content"):
            return {"success": False, "announcement": None, "error": "title and content are required"}
        announcement = Announcement.update(announcement_id, data)
        if announcement is None:
            return {"success": False, "announcement": None, "error": f"Announcement {announcement_id} not found"}
        return {"success": True, "announcement": announcement.to_dict(), "error": None}

    @staticmethod
    def partial_update(announcement_id: int, data: dict) -> dict:
        announcement = Announcement.partial_update(announcement_id, data)
        if announcement is None:
            return {"success": False, "announcement": None, "error": f"Announcement {announcement_id} not found"}
        return {"success": True, "announcement": announcement.to_dict(), "error": None}

    @staticmethod
    def delete(announcement_id: int) -> dict:
        deleted = Announcement.delete(announcement_id)
        if not deleted:
            return {"success": False, "message": f"Announcement {announcement_id} not found"}
        return {"success": True, "message": f"Announcement {announcement_id} deleted"}
