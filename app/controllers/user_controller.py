"""
UserController — HTML / web-facing controller with database connection.

Handles user-facing routes that return HTML responses.
Delegates all data operations to the SQLAlchemy User model.
"""

from app.models.user import User


class UserController:

    # ------------------------------------------------------------------
    # CREATE — process form submission
    # ------------------------------------------------------------------

    @staticmethod
    def create(data: dict) -> dict:
        """
        Create a new user from form data with database uniqueness checks.
        """
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()

        if not name or not email:
            return {"success": False, "user": None, "error": "Name and email are required"}

        # Database constraint check
        existing = User.query.filter_by(email=email).first()
        if existing:
            return {"success": False, "user": None, "error": f"Email '{email}' is already registered in the database"}

        try:
            user = User.create({
                "name": name,
                "email": email,
                "status": data.get("status", "student"),
                "department": data.get("department"),
                "graduation_year": data.get("graduation_year"),
            })
            return {"success": True, "user": user.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "user": None, "error": f"Database error: {str(e)}"}

    # ------------------------------------------------------------------
    # READ ALL — list page
    # ------------------------------------------------------------------

    @staticmethod
    def index() -> dict:
        """
        Retrieve all users from the database.
        """
        return {"success": True, "users": User.get_all()}

    # ------------------------------------------------------------------
    # READ ONE — detail page
    # ------------------------------------------------------------------

    @staticmethod
    def show(user_id: int) -> dict:
        """
        Retrieve a single user by ID from the database.
        """
        user = User.get_by_id(user_id)
        if user is None:
            return {"success": False, "user": None, "error": f"User {user_id} not found in database"}
        return {"success": True, "user": user.to_dict(), "error": None}

    # ------------------------------------------------------------------
    # UPDATE (full replace)
    # ------------------------------------------------------------------

    @staticmethod
    def update(user_id: int, data: dict) -> dict:
        """
        Fully replace a user's fields in the database with conflict checking.
        """
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()

        if not name or not email:
            return {"success": False, "user": None, "error": "Name and email are required"}

        # Database conflict check: ensure email is not taken by another user
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user_id:
            return {"success": False, "user": None, "error": f"Email '{email}' is already in use by another user"}

        try:
            user = User.update(user_id, {
                "name": name,
                "email": email,
                "status": data.get("status", "student"),
                "department": data.get("department"),
                "graduation_year": data.get("graduation_year"),
            })
            if user is None:
                return {"success": False, "user": None, "error": f"User {user_id} not found in database"}
            return {"success": True, "user": user.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "user": None, "error": f"Database error: {str(e)}"}

    # ------------------------------------------------------------------
    # PARTIAL UPDATE
    # ------------------------------------------------------------------

    @staticmethod
    def partial_update(user_id: int, data: dict) -> dict:
        """
        Update only the provided fields of a user in the database.
        """
        email = data.get("email")
        if email:
            email = email.strip().lower()
            existing = User.query.filter_by(email=email).first()
            if existing and existing.id != user_id:
                return {"success": False, "user": None, "error": f"Email '{email}' is already in use by another user"}
            data["email"] = email

        try:
            user = User.partial_update(user_id, data)
            if user is None:
                return {"success": False, "user": None, "error": f"User {user_id} not found in database"}
            return {"success": True, "user": user.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "user": None, "error": f"Database error: {str(e)}"}

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    @staticmethod
    def delete(user_id: int) -> dict:
        """
        Delete a user by ID from the database.
        """
        try:
            deleted = User.delete(user_id)
            if not deleted:
                return {"success": False, "message": f"User {user_id} not found in database"}
            return {"success": True, "message": f"User {user_id} deleted successfully"}
        except Exception as e:
            return {"success": False, "message": f"Database error: {str(e)}"}
