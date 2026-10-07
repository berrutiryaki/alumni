"""
UserController — HTML / web-facing controller.

Handles user-facing routes that return HTML responses.
Delegates all data operations to the User model.
"""

from app.models.user import User


class UserController:

    # ------------------------------------------------------------------
    # CREATE — render a form or process form submission
    # ------------------------------------------------------------------

    @staticmethod
    def create(data: dict) -> dict:
        """
        Create a new user from form data.

        Args:
            data: dict with keys: name, email, department, graduation_year

        Returns:
            dict with keys: success (bool), user (dict | None), error (str | None)
        """
        if not data.get("name") or not data.get("email"):
            return {"success": False, "user": None, "error": "name and email are required"}

        user = User.create(data)
        return {"success": True, "user": user.to_dict(), "error": None}

    # ------------------------------------------------------------------
    # READ ALL — list page
    # ------------------------------------------------------------------

    @staticmethod
    def index() -> dict:
        """
        Retrieve all users.

        Returns:
            dict with keys: success (bool), users (list[dict])
        """
        return {"success": True, "users": User.get_all()}

    # ------------------------------------------------------------------
    # READ ONE — detail page
    # ------------------------------------------------------------------

    @staticmethod
    def show(user_id: int) -> dict:
        """
        Retrieve a single user by ID.

        Args:
            user_id: int

        Returns:
            dict with keys: success (bool), user (dict | None), error (str | None)
        """
        user = User.get_by_id(user_id)
        if user is None:
            return {"success": False, "user": None, "error": f"User {user_id} not found"}
        return {"success": True, "user": user.to_dict(), "error": None}

    # ------------------------------------------------------------------
    # UPDATE (full replace)
    # ------------------------------------------------------------------

    @staticmethod
    def update(user_id: int, data: dict) -> dict:
        """
        Fully replace a user's fields.

        Args:
            user_id: int
            data: dict with new field values

        Returns:
            dict with keys: success (bool), user (dict | None), error (str | None)
        """
        if not data.get("name") or not data.get("email"):
            return {"success": False, "user": None, "error": "name and email are required"}

        user = User.update(user_id, data)
        if user is None:
            return {"success": False, "user": None, "error": f"User {user_id} not found"}
        return {"success": True, "user": user.to_dict(), "error": None}

    # ------------------------------------------------------------------
    # PARTIAL UPDATE
    # ------------------------------------------------------------------

    @staticmethod
    def partial_update(user_id: int, data: dict) -> dict:
        """
        Update only the provided fields of a user.

        Args:
            user_id: int
            data: dict with only the fields to change

        Returns:
            dict with keys: success (bool), user (dict | None), error (str | None)
        """
        user = User.partial_update(user_id, data)
        if user is None:
            return {"success": False, "user": None, "error": f"User {user_id} not found"}
        return {"success": True, "user": user.to_dict(), "error": None}

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    @staticmethod
    def delete(user_id: int) -> dict:
        """
        Delete a user by ID.

        Args:
            user_id: int

        Returns:
            dict with keys: success (bool), message (str)
        """
        deleted = User.delete(user_id)
        if not deleted:
            return {"success": False, "message": f"User {user_id} not found"}
        return {"success": True, "message": f"User {user_id} deleted"}
