"""
JobPosting Model — SQLAlchemy database model with migration support.
Independent model representing job opportunities, linked to applicants via Application action table.
"""

from datetime import datetime
from app.database import db


class JobPosting(db.Model):
    __tablename__ = "job_postings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=True)
    employment_type = db.Column(db.String(50), nullable=False, default="full-time")
    salary_range = db.Column(db.String(100), nullable=True)
    posted_by = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.String(30), nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    expires_at = db.Column(db.String(50), nullable=True)

    # ------------------------------------------------------------------
    # Action Table Relationships (Many-to-Many via Application)
    # ------------------------------------------------------------------
    applications = db.relationship("Application", back_populates="job_posting", lazy="dynamic")

    def __init__(self, title: str, description: str, company: str,
                 location: str = None, employment_type: str = "full-time",
                 salary_range: str = None, posted_by: str = None,
                 is_active: bool = True, expires_at: str = None):
        self.title = title
        self.description = description
        self.company = company
        self.location = location
        self.employment_type = employment_type or "full-time"
        self.salary_range = salary_range
        self.posted_by = posted_by
        self.is_active = is_active
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.expires_at = expires_at

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "company": self.company,
            "location": self.location,
            "employment_type": self.employment_type,
            "salary_range": self.salary_range,
            "posted_by": self.posted_by,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
        }

    # ------------------------------------------------------------------
    # CRUD helpers for seamless controller/route integration
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, data: dict) -> "JobPosting":
        jp = cls(
            title=data.get("title"),
            description=data.get("description"),
            company=data.get("company"),
            location=data.get("location"),
            employment_type=data.get("employment_type", "full-time"),
            salary_range=data.get("salary_range"),
            posted_by=data.get("posted_by"),
            is_active=data.get("is_active", True) not in [False, "false", "0", 0],
            expires_at=data.get("expires_at"),
        )
        try:
            db.session.add(jp)
            db.session.commit()
            return jp
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def get_all(cls) -> list:
        return [jp.to_dict() for jp in cls.query.order_by(cls.id.asc()).all()]

    @classmethod
    def get_by_id(cls, job_posting_id: int) -> "JobPosting | None":
        return db.session.get(cls, job_posting_id)

    @classmethod
    def update(cls, job_posting_id: int, data: dict) -> "JobPosting | None":
        jp = cls.get_by_id(job_posting_id)
        if jp is None:
            return None
        jp.title = data.get("title")
        jp.description = data.get("description")
        jp.company = data.get("company")
        jp.location = data.get("location")
        jp.employment_type = data.get("employment_type", "full-time")
        jp.salary_range = data.get("salary_range")
        jp.posted_by = data.get("posted_by")
        jp.is_active = data.get("is_active", True) not in [False, "false", "0", 0]
        jp.expires_at = data.get("expires_at")
        try:
            db.session.commit()
            return jp
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def partial_update(cls, job_posting_id: int, data: dict) -> "JobPosting | None":
        jp = cls.get_by_id(job_posting_id)
        if jp is None:
            return None
        if "title" in data:
            jp.title = data["title"]
        if "description" in data:
            jp.description = data["description"]
        if "company" in data:
            jp.company = data["company"]
        if "location" in data:
            jp.location = data["location"]
        if "employment_type" in data:
            jp.employment_type = data["employment_type"]
        if "salary_range" in data:
            jp.salary_range = data["salary_range"]
        if "posted_by" in data:
            jp.posted_by = data["posted_by"]
        if "is_active" in data:
            jp.is_active = data["is_active"] not in [False, "false", "0", 0]
        if "expires_at" in data:
            jp.expires_at = data["expires_at"]
        try:
            db.session.commit()
            return jp
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def delete(cls, job_posting_id: int) -> bool:
        jp = cls.get_by_id(job_posting_id)
        if jp is None:
            return False
        try:
            db.session.delete(jp)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    def __repr__(self) -> str:
        return f"<JobPosting id={self.id} title={self.title!r} company={self.company!r}>"
