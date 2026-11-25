"""
User Model — SQLAlchemy database model with migration support.
Supports role-based user accounts (student, alumni, academician, admin) and hashed passwords.
"""

from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db

VALID_ROLES = ("student", "alumni", "academician", "admin")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(30), nullable=False, default="student")
    status = db.Column(db.String(20), nullable=False, default="student")  # kept in sync with role
    department = db.Column(db.String(120), nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)
    company = db.Column(db.String(120), nullable=True)
    job_title = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    announcements = db.relationship("Announcement", back_populates="user", lazy="dynamic")
    applications = db.relationship("Application", back_populates="user", lazy="dynamic")

    def __init__(self, name: str, email: str, status: str = None, role: str = None,
                 department: str = None, graduation_year: int = None,
                 password: str = None, password_hash: str = None,
                 company: str = None, job_title: str = None,
                 location: str = None, linkedin_url: str = None):
        resolved_role = (role or status or "student").strip().lower()
        if resolved_role not in VALID_ROLES:
            resolved_role = "student"

        self.name = name
        self.email = email
        self.role = resolved_role
        self.status = resolved_role
        self.department = department
        self.graduation_year = self._normalize_grad_year(graduation_year, resolved_role)
        self.company = company
        self.job_title = job_title
        self.location = location
        self.linkedin_url = linkedin_url

        if password:
            self.set_password(password)
        elif password_hash:
            self.password_hash = password_hash

    @staticmethod
    def _normalize_grad_year(graduation_year, role: str) -> int | None:
        if role != "alumni" or graduation_year in (None, ""):
            return None
        try:
            return int(graduation_year)
        except (ValueError, TypeError):
            return None

    # ------------------------------------------------------------------
    # Password helpers (Werkzeug security)
    # ------------------------------------------------------------------

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return (self.role or "").strip().lower() == "admin"

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role or self.status,
            "status": self.role or self.status,
            "department": self.department,
            "graduation_year": self.graduation_year,
            "company": self.company,
            "job_title": self.job_title,
            "location": self.location,
            "linkedin_url": self.linkedin_url,
        }

    # ------------------------------------------------------------------
    # CRUD helpers for seamless controller/route integration
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, data: dict) -> "User":
        role = data.get("role") or data.get("status") or "student"
        user = cls(
            name=data.get("name"),
            email=data.get("email"),
            role=role,
            status=role,
            department=data.get("department"),
            graduation_year=data.get("graduation_year"),
            password=data.get("password"),
            password_hash=data.get("password_hash"),
        )
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def get_all(cls) -> list:
        return [u.to_dict() for u in cls.query.order_by(cls.id.asc()).all()]

    @classmethod
    def get_by_id(cls, user_id: int) -> "User | None":
        return db.session.get(cls, user_id)

    @classmethod
    def update(cls, user_id: int, data: dict) -> "User | None":
        user = cls.get_by_id(user_id)
        if user is None:
            return None
        resolved_role = (data.get("role") or data.get("status") or user.role or "student").strip().lower()
        if resolved_role not in VALID_ROLES:
            resolved_role = "student"

        user.name = data.get("name")
        user.email = data.get("email")
        user.role = resolved_role
        user.status = resolved_role
        user.department = data.get("department")
        user.graduation_year = cls._normalize_grad_year(data.get("graduation_year"), resolved_role)
        if data.get("password"):
            user.set_password(data["password"])
        try:
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def partial_update(cls, user_id: int, data: dict) -> "User | None":
        user = cls.get_by_id(user_id)
        if user is None:
            return None
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "role" in data or "status" in data:
            resolved_role = (data.get("role") or data.get("status") or "student").strip().lower()
            if resolved_role in VALID_ROLES:
                user.role = resolved_role
                user.status = resolved_role
            if user.role != "alumni":
                user.graduation_year = None
        if "department" in data:
            user.department = data["department"]
        if "graduation_year" in data:
            user.graduation_year = cls._normalize_grad_year(data["graduation_year"], user.role)
        if "company" in data:
            user.company = data["company"]
        if "job_title" in data:
            user.job_title = data["job_title"]
        if "location" in data:
            user.location = data["location"]
        if "linkedin_url" in data:
            user.linkedin_url = data["linkedin_url"]
        if data.get("password"):
            user.set_password(data["password"])
        try:
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def delete(cls, user_id: int) -> bool:
        user = cls.get_by_id(user_id)
        if user is None:
            return False
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r} role={self.role!r}>"
