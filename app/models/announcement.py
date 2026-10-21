"""
Announcement Model — SQLAlchemy database model with migration support.
"""

from datetime import datetime
from app.database import db


class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(120), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.String(30), nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    # ------------------------------------------------------------------
    # Foreign Keys & Relationships
    # ------------------------------------------------------------------
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship("User", back_populates="announcements")

    def __init__(self, title: str, content: str, author: str = None,
                 is_active: bool = True, user_id: int = None):
        self.title = title
        self.content = content
        self.author = author
        self.is_active = is_active
        self.user_id = user_id
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
            "user_id": self.user_id,
        }

    # ------------------------------------------------------------------
    # CRUD helpers for seamless controller/route integration
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, data: dict) -> "Announcement":
        user_id = data.get("user_id")
        if user_id is not None:
            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                user_id = None
        a = cls(
            title=data.get("title"),
            content=data.get("content"),
            author=data.get("author"),
            is_active=data.get("is_active", True) not in [False, "false", "0", 0],
            user_id=user_id,
        )
        try:
            db.session.add(a)
            db.session.commit()
            return a
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def get_all(cls) -> list:
        return [a.to_dict() for a in cls.query.order_by(cls.id.asc()).all()]

    @classmethod
    def get_by_id(cls, announcement_id: int) -> "Announcement | None":
        return db.session.get(cls, announcement_id)

    @classmethod
    def update(cls, announcement_id: int, data: dict) -> "Announcement | None":
        a = cls.get_by_id(announcement_id)
        if a is None:
            return None
        a.title = data.get("title")
        a.content = data.get("content")
        a.author = data.get("author")
        a.is_active = data.get("is_active", True) not in [False, "false", "0", 0]
        if "user_id" in data:
            user_id = data["user_id"]
            try:
                a.user_id = int(user_id) if user_id else None
            except (ValueError, TypeError):
                a.user_id = None
        try:
            db.session.commit()
            return a
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def partial_update(cls, announcement_id: int, data: dict) -> "Announcement | None":
        a = cls.get_by_id(announcement_id)
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
        if "user_id" in data:
            user_id = data["user_id"]
            try:
                a.user_id = int(user_id) if user_id else None
            except (ValueError, TypeError):
                a.user_id = None
        try:
            db.session.commit()
            return a
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def delete(cls, announcement_id: int) -> bool:
        a = cls.get_by_id(announcement_id)
        if a is None:
            return False
        try:
            db.session.delete(a)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    def __repr__(self) -> str:
        return f"<Announcement id={self.id} title={self.title!r}>"

