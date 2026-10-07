"""
Announcement Model — in-memory, no database connection.

Stores all announcements in a module-level list.
Provides static CRUD methods that operate on that list.
"""

from datetime import datetime


class Announcement:
    _store: list = []
    _next_id: int = 1

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

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, data: dict) -> "Announcement":
        announcement = cls(
            title=data.get("title"),
            content=data.get("content"),
            author=data.get("author"),
            is_active=data.get("is_active", True) not in [False, "false", "0", 0],
        )
        announcement.id = cls._next_id
        cls._next_id += 1
        cls._store.append(announcement)
        return announcement

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    @classmethod
    def get_all(cls) -> list:
        return [a.to_dict() for a in cls._store]

    @classmethod
    def get_by_id(cls, announcement_id: int) -> "Announcement | None":
        return next((a for a in cls._store if a.id == announcement_id), None)

    # ------------------------------------------------------------------
    # UPDATE (full replace)
    # ------------------------------------------------------------------

    @classmethod
    def update(cls, announcement_id: int, data: dict) -> "Announcement | None":
        announcement = cls.get_by_id(announcement_id)
        if announcement is None:
            return None
        announcement.title = data.get("title")
        announcement.content = data.get("content")
        announcement.author = data.get("author")
        announcement.is_active = data.get("is_active", True) not in [False, "false", "0", 0]
        return announcement

    # ------------------------------------------------------------------
    # PARTIAL UPDATE
    # ------------------------------------------------------------------

    @classmethod
    def partial_update(cls, announcement_id: int, data: dict) -> "Announcement | None":
        announcement = cls.get_by_id(announcement_id)
        if announcement is None:
            return None
        if "title" in data:
            announcement.title = data["title"]
        if "content" in data:
            announcement.content = data["content"]
        if "author" in data:
            announcement.author = data["author"]
        if "is_active" in data:
            announcement.is_active = data["is_active"] not in [False, "false", "0", 0]
        return announcement

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    @classmethod
    def delete(cls, announcement_id: int) -> bool:
        announcement = cls.get_by_id(announcement_id)
        if announcement is None:
            return False
        cls._store.remove(announcement)
        return True

    def __repr__(self) -> str:
        return f"<Announcement id={self.id} title={self.title!r}>"
