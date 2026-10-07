"""
User Model — in-memory, no database connection.

Stores all users in a module-level list.
Provides static CRUD methods that operate on that list.
"""


class User:
    _store: list = []   # in-memory storage shared across all instances
    _next_id: int = 1   # auto-increment counter

    def __init__(self, name: str, email: str, department: str = None, graduation_year: int = None):
        self.id = None          # assigned by create()
        self.name = name
        self.email = email
        self.department = department
        self.graduation_year = graduation_year

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a plain dict representation of this user."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "graduation_year": self.graduation_year,
        }

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, data: dict) -> "User":
        """
        Create a new User from a dict, assign an auto-incremented ID,
        persist to the in-memory store, and return the instance.
        """
        user = cls(
            name=data.get("name"),
            email=data.get("email"),
            department=data.get("department"),
            graduation_year=data.get("graduation_year"),
        )
        user.id = cls._next_id
        cls._next_id += 1
        cls._store.append(user)
        return user

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    @classmethod
    def get_all(cls) -> list:
        """Return all users as a list of dicts."""
        return [u.to_dict() for u in cls._store]

    @classmethod
    def get_by_id(cls, user_id: int) -> "User | None":
        """Return the User instance with the given ID, or None if not found."""
        return next((u for u in cls._store if u.id == user_id), None)

    # ------------------------------------------------------------------
    # UPDATE (full replace)
    # ------------------------------------------------------------------

    @classmethod
    def update(cls, user_id: int, data: dict) -> "User | None":
        """
        Fully replace all fields of the user with the given ID.
        Returns the updated User instance, or None if not found.
        """
        user = cls.get_by_id(user_id)
        if user is None:
            return None
        user.name = data.get("name")
        user.email = data.get("email")
        user.department = data.get("department")
        user.graduation_year = data.get("graduation_year")
        return user

    # ------------------------------------------------------------------
    # PARTIAL UPDATE (patch)
    # ------------------------------------------------------------------

    @classmethod
    def partial_update(cls, user_id: int, data: dict) -> "User | None":
        """
        Update only the fields present in data, leaving others unchanged.
        Returns the updated User instance, or None if not found.
        """
        user = cls.get_by_id(user_id)
        if user is None:
            return None
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "department" in data:
            user.department = data["department"]
        if "graduation_year" in data:
            user.graduation_year = data["graduation_year"]
        return user

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    @classmethod
    def delete(cls, user_id: int) -> bool:
        """
        Remove the user with the given ID from the store.
        Returns True if deleted, False if not found.
        """
        user = cls.get_by_id(user_id)
        if user is None:
            return False
        cls._store.remove(user)
        return True

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r} email={self.email!r}>"
