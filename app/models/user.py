"""
User Model — JSON-backed persistence, no database connection.

Stores all users in a JSON file via app.storage.
Provides static CRUD methods that operate on that file.
"""

from app.storage import load, save

_FILE = "users.json"


class User:
    _next_id: int = 1

    def __init__(self, name: str, email: str, status: str = "student",
                 department: str = None, graduation_year: int = None):
        self.id = None
        self.name = name
        self.email = email
        self.status = status        # 'alumni' or 'student'
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

    @classmethod
    def _from_dict(cls, d: dict) -> "User":
        u = cls(
            name=d["name"],
            email=d["email"],
            status=d.get("status", "student"),
            department=d.get("department"),
            graduation_year=d.get("graduation_year"),
        )
        u.id = d["id"]
        u.graduation_year = d.get("graduation_year")   # preserve stored value
        return u

    # ------------------------------------------------------------------
    # Storage helpers
    # ------------------------------------------------------------------

    @classmethod
    def _load(cls) -> list:
        return [cls._from_dict(d) for d in load(_FILE)]

    @classmethod
    def _save(cls, users: list) -> None:
        save(_FILE, [u.to_dict() for u in users])

    @classmethod
    def _next(cls, users: list) -> int:
        return max((u.id for u in users), default=0) + 1

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, data: dict) -> "User":
        users = cls._load()
        user = cls(
            name=data.get("name"),
            email=data.get("email"),
            status=data.get("status", "student"),
            department=data.get("department"),
            graduation_year=data.get("graduation_year"),
        )
        user.id = cls._next(users)
        users.append(user)
        cls._save(users)
        return user

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    @classmethod
    def get_all(cls) -> list:
        return [u.to_dict() for u in cls._load()]

    @classmethod
    def get_by_id(cls, user_id: int) -> "User | None":
        return next((u for u in cls._load() if u.id == user_id), None)

    # ------------------------------------------------------------------
    # UPDATE (full replace)
    # ------------------------------------------------------------------

    @classmethod
    def update(cls, user_id: int, data: dict) -> "User | None":
        users = cls._load()
        user = next((u for u in users if u.id == user_id), None)
        if user is None:
            return None
        user.name = data.get("name")
        user.email = data.get("email")
        user.status = data.get("status", "student")
        user.department = data.get("department")
        user.graduation_year = data.get("graduation_year") if user.status == "alumni" else None
        cls._save(users)
        return user

    # ------------------------------------------------------------------
    # PARTIAL UPDATE
    # ------------------------------------------------------------------

    @classmethod
    def partial_update(cls, user_id: int, data: dict) -> "User | None":
        users = cls._load()
        user = next((u for u in users if u.id == user_id), None)
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
        cls._save(users)
        return user

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    @classmethod
    def delete(cls, user_id: int) -> bool:
        users = cls._load()
        user = next((u for u in users if u.id == user_id), None)
        if user is None:
            return False
        users.remove(user)
        cls._save(users)
        return True

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r}>"
