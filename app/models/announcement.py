"""
Announcement Model — JSON-backed persistence, no database connection.

Stores all announcements in a JSON file via app.storage.
Provides static CRUD methods that operate on that file.
"""

from datetime import datetime
from app.storage import load, save

_FILE = "announcements.json"


class Announcement:

    def __init__(self, title: str, content: str, author: str = None, is_active: bool = True):
        self.id = None
        self.title = title
        self.content = content
        self.author = author
        self.is_active = is_active
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "is_active": self.is_active,
            "created_at": self.created_at,
        }

    @classmethod
    def _from_dict(cls, d: dict) -> "Announcement":
        a = cls(
            title=d["title"],
            content=d["content"],
            author=d.get("author"),
            is_active=d.get("is_active", True),
        )
        a.id = d["id"]
        a.created_at = d.get("created_at", a.created_at)
        return a

    # ------------------------------------------------------------------
    # Storage helpers
    # ------------------------------------------------------------------

    @classmethod
    def _load(cls) -> list:
        return [cls._from_dict(d) for d in load(_FILE)]

    @classmethod
    def _save(cls, announcements: list) -> None:
        save(_FILE, [a.to_dict() for a in announcements])

    @classmethod
    def _next(cls, announcements: list) -> int:
        return max((a.id for a in announcements), default=0) + 1

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, data: dict) -> "Announcement":
        announcements = cls._load()
        a = cls(
            title=data.get("title"),
            content=data.get("content"),
            author=data.get("author"),
            is_active=data.get("is_active", True) not in [False, "false", "0", 0],
        )
        a.id = cls._next(announcements)
        announcements.append(a)
        cls._save(announcements)
        return a

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    @classmethod
    def get_all(cls) -> list:
        return [a.to_dict() for a in cls._load()]

    @classmethod
    def get_by_id(cls, announcement_id: int) -> "Announcement | None":
        return next((a for a in cls._load() if a.id == announcement_id), None)

    # ------------------------------------------------------------------
    # UPDATE (full replace)
    # ------------------------------------------------------------------

    @classmethod
    def update(cls, announcement_id: int, data: dict) -> "Announcement | None":
        announcements = cls._load()
        a = next((a for a in announcements if a.id == announcement_id), None)
        if a is None:
            return None
        a.title = data.get("title")
        a.content = data.get("content")
        a.author = data.get("author")
        a.is_active = data.get("is_active", True) not in [False, "false", "0", 0]
        cls._save(announcements)
        return a

    # ------------------------------------------------------------------
    # PARTIAL UPDATE
    # ------------------------------------------------------------------

    @classmethod
    def partial_update(cls, announcement_id: int, data: dict) -> "Announcement | None":
        announcements = cls._load()
        a = next((a for a in announcements if a.id == announcement_id), None)
        if a is None:
            return None
        if "title" in data:
            a.title = data["title"]
        if "content" in data:
            a.content = data["content"]
        if "author" in data:
            a.author = data["author"]
        if "is_active" in data:
            a.is_active = data["is_active"] not in [False, "false", "0", 0]
        cls._save(announcements)
        return a

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    @classmethod
    def delete(cls, announcement_id: int) -> bool:
        announcements = cls._load()
        a = next((a for a in announcements if a.id == announcement_id), None)
        if a is None:
            return False
        announcements.remove(a)
        cls._save(announcements)
        return True

    def __repr__(self) -> str:
        return f"<Announcement id={self.id} title={self.title!r}>"
