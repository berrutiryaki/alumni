"""
User Model — SQLAlchemy database model with migration support.
"""

from app.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="student")  # 'alumni' or 'student'
    department = db.Column(db.String(120), nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)

    def __init__(self, name: str, email: str, status: str = "student",
                 department: str = None, graduation_year: int = None):
        self.name = name
        self.email = email
        self.status = status
        self.department = department
        self.graduation_year = graduation_year if status == "alumni" else None

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "status": self.status,
            "department": self.department,
            "graduation_year": self.graduation_year,
        }

    # ------------------------------------------------------------------
    # CRUD helpers for seamless controller/route integration
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, data: dict) -> "User":
        user = cls(
            name=data.get("name"),
            email=data.get("email"),
            status=data.get("status", "student"),
            department=data.get("department"),
            graduation_year=data.get("graduation_year"),
        )
        db.session.add(user)
        db.session.commit()
        return user

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
        user.name = data.get("name")
        user.email = data.get("email")
        user.status = data.get("status", "student")
        user.department = data.get("department")
        user.graduation_year = data.get("graduation_year") if user.status == "alumni" else None
        db.session.commit()
        return user

    @classmethod
    def partial_update(cls, user_id: int, data: dict) -> "User | None":
        user = cls.get_by_id(user_id)
        if user is None:
            return None
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "status" in data:
            user.status = data["status"]
            if user.status != "alumni":
                user.graduation_year = None
        if "department" in data:
            user.department = data["department"]
        if "graduation_year" in data and user.status == "alumni":
            user.graduation_year = data["graduation_year"]
        db.session.commit()
        return user

    @classmethod
    def delete(cls, user_id: int) -> bool:
        user = cls.get_by_id(user_id)
        if user is None:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r}>"
