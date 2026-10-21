"""
Application Model — SQLAlchemy database model with migration support.
Represents a job application submitted by a user for a specific job posting.
"""

from datetime import datetime
from app.database import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_posting_id = db.Column(db.Integer, db.ForeignKey("job_postings.id"), nullable=False)
    resume_url = db.Column(db.String(255), nullable=True)
    cover_letter = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="pending")  # pending, reviewed, accepted, rejected
    applied_at = db.Column(db.String(30), nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    # ------------------------------------------------------------------
    # Foreign Keys & Relationships
    # ------------------------------------------------------------------
    user = db.relationship("User", back_populates="applications")
    job_posting = db.relationship("JobPosting", back_populates="applications")

    def __init__(self, user_id: int, job_posting_id: int, resume_url: str = None,
                 cover_letter: str = None, status: str = "pending"):
        self.user_id = user_id
        self.job_posting_id = job_posting_id
        self.resume_url = resume_url
        self.cover_letter = cover_letter
        self.status = status or "pending"
        self.applied_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_posting_id": self.job_posting_id,
            "resume_url": self.resume_url,
            "cover_letter": self.cover_letter,
            "status": self.status,
            "applied_at": self.applied_at,
            "user_name": self.user.name if self.user else None,
            "job_title": self.job_posting.title if self.job_posting else None,
            "company": self.job_posting.company if self.job_posting else None,
        }

    # ------------------------------------------------------------------
    # CRUD helpers for seamless controller/route integration
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, data: dict) -> "Application":
        app_rec = cls(
            user_id=int(data.get("user_id")),
            job_posting_id=int(data.get("job_posting_id")),
            resume_url=data.get("resume_url"),
            cover_letter=data.get("cover_letter"),
            status=data.get("status", "pending") or "pending",
        )
        try:
            db.session.add(app_rec)
            db.session.commit()
            return app_rec
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def get_all(cls) -> list:
        return [a.to_dict() for a in cls.query.order_by(cls.id.asc()).all()]

    @classmethod
    def get_by_id(cls, application_id: int) -> "Application | None":
        return db.session.get(cls, application_id)

    @classmethod
    def update(cls, application_id: int, data: dict) -> "Application | None":
        app_rec = cls.get_by_id(application_id)
        if app_rec is None:
            return None
        app_rec.user_id = int(data.get("user_id"))
        app_rec.job_posting_id = int(data.get("job_posting_id"))
        app_rec.resume_url = data.get("resume_url")
        app_rec.cover_letter = data.get("cover_letter")
        app_rec.status = data.get("status", "pending") or "pending"
        try:
            db.session.commit()
            return app_rec
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def partial_update(cls, application_id: int, data: dict) -> "Application | None":
        app_rec = cls.get_by_id(application_id)
        if app_rec is None:
            return None
        if "user_id" in data:
            app_rec.user_id = int(data["user_id"])
        if "job_posting_id" in data:
            app_rec.job_posting_id = int(data["job_posting_id"])
        if "resume_url" in data:
            app_rec.resume_url = data["resume_url"]
        if "cover_letter" in data:
            app_rec.cover_letter = data["cover_letter"]
        if "status" in data:
            app_rec.status = data["status"]
        try:
            db.session.commit()
            return app_rec
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def delete(cls, application_id: int) -> bool:
        app_rec = cls.get_by_id(application_id)
        if app_rec is None:
            return False
        try:
            db.session.delete(app_rec)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    def __repr__(self) -> str:
        return f"<Application id={self.id} user_id={self.user_id} job_posting_id={self.job_posting_id}>"
