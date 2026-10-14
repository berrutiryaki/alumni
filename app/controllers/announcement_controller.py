"""
AnnouncementController — HTML / web-facing controller with database connection.

Delegates all data operations to the SQLAlchemy Announcement model.
Returns plain dicts consumed by the web route layer.
"""

from app.models.announcement import Announcement


class AnnouncementController:

    @staticmethod
    def index() -> dict:
        try:
            return {"success": True, "announcements": Announcement.get_all()}
        except Exception as e:
            return {"success": False, "announcements": [], "error": f"Database error: {str(e)}"}

    @staticmethod
    def show(announcement_id: int) -> dict:
        try:
            announcement = Announcement.get_by_id(announcement_id)
            if announcement is None:
                return {"success": False, "announcement": None, "error": f"Announcement {announcement_id} not found"}
            return {"success": True, "announcement": announcement.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "announcement": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def create(data: dict) -> dict:
        title = (data.get("title") or "").strip()
        content = (data.get("content") or "").strip()

        if not title or not content:
            return {"success": False, "announcement": None, "error": "Title and content are required"}

        try:
            announcement = Announcement.create({
                "title": title,
                "content": content,
                "author": (data.get("author") or "").strip() or None,
                "is_active": data.get("is_active", True) not in [False, "false", "0", 0],
            })
            return {"success": True, "announcement": announcement.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "announcement": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def update(announcement_id: int, data: dict) -> dict:
        title = (data.get("title") or "").strip()
        content = (data.get("content") or "").strip()

        if not title or not content:
            return {"success": False, "announcement": None, "error": "Title and content are required"}

        try:
            announcement = Announcement.update(announcement_id, {
                "title": title,
                "content": content,
                "author": (data.get("author") or "").strip() or None,
                "is_active": data.get("is_active", True) not in [False, "false", "0", 0],
            })
            if announcement is None:
                return {"success": False, "announcement": None, "error": f"Announcement {announcement_id} not found"}
            return {"success": True, "announcement": announcement.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "announcement": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def partial_update(announcement_id: int, data: dict) -> dict:
        try:
            announcement = Announcement.partial_update(announcement_id, data)
            if announcement is None:
                return {"success": False, "announcement": None, "error": f"Announcement {announcement_id} not found"}
            return {"success": True, "announcement": announcement.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "announcement": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def delete(announcement_id: int) -> dict:
        try:
            deleted = Announcement.delete(announcement_id)
            if not deleted:
                return {"success": False, "message": f"Announcement {announcement_id} not found"}
            return {"success": True, "message": f"Announcement {announcement_id} deleted successfully"}
        except Exception as e:
            return {"success": False, "message": f"Database error: {str(e)}"}
