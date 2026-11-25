"""
UserController — HTML / web-facing controller with database connection.

Handles user-facing routes that return HTML responses (including /register).
Delegates all data operations to the SQLAlchemy User model.
"""

from werkzeug.security import generate_password_hash
from app.models.user import User, VALID_ROLES


class UserController:

    # ------------------------------------------------------------------
    # LOGIN — authenticate user credentials (POST /login)
    # ------------------------------------------------------------------

    @staticmethod
    def login(data: dict) -> dict:
        """
        Authenticate user by email and password using werkzeug.security.check_password_hash.
        """
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not email or not password:
            return {
                "success": False,
                "user": None,
                "error": "Please enter both your email address and password.",
            }

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            return {
                "success": False,
                "user": None,
                "error": "Invalid email or password. Please check your credentials and try again.",
            }

        return {"success": True, "user": user.to_dict(), "error": None}

    # ------------------------------------------------------------------
    # REGISTER — process registration form submission (POST /register)
    # ------------------------------------------------------------------

    @staticmethod
    def register(data: dict) -> dict:
        """
        Validate registration fields per ddd.md rules, hash password with
        werkzeug.security.generate_password_hash, and persist user.
        """
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        confirm_password = data.get("confirm_password") or ""
        role = (data.get("role") or data.get("status") or "").strip().lower()
        department = (data.get("department") or "").strip() or None
        graduation_year_raw = (str(data.get("graduation_year") or "")).strip()

        if not name or not email or not password or not confirm_password or not role:
            return {
                "success": False,
                "user": None,
                "error": "Please fill in all required fields (Name, Email, Password, Confirm Password, and Role).",
            }

        if role not in VALID_ROLES:
            return {
                "success": False,
                "user": None,
                "error": f"Invalid role '{role}'. Allowed roles: {', '.join(VALID_ROLES)}.",
            }

        if password != confirm_password:
            return {
                "success": False,
                "user": None,
                "error": "Passwords do not match. Please enter matching passwords.",
            }

        if len(password) < 6:
            return {
                "success": False,
                "user": None,
                "error": "Password must be at least 6 characters long.",
            }

        graduation_year = None
        if role == "alumni" and graduation_year_raw:
            try:
                graduation_year = int(graduation_year_raw)
                if graduation_year < 1900 or graduation_year > 2100:
                    raise ValueError()
            except ValueError:
                return {
                    "success": False,
                    "user": None,
                    "error": "Graduation year must be a valid 4-digit year between 1900 and 2100.",
                }

        existing = User.query.filter_by(email=email).first()
        if existing:
            return {
                "success": False,
                "user": None,
                "error": f"Email '{email}' is already registered in the database.",
            }

        password_hash = generate_password_hash(password)

        try:
            user = User.create({
                "name": name,
                "email": email,
                "password_hash": password_hash,
                "role": role,
                "status": role,
                "department": department,
                "graduation_year": graduation_year,
            })
            return {"success": True, "user": user.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "user": None, "error": f"Database error: {str(e)}"}

    # ------------------------------------------------------------------
    # CREATE — process admin/directory form submission
    # ------------------------------------------------------------------

    @staticmethod
    def create(data: dict) -> dict:
        """
        Create a new user from form data with database uniqueness checks.
        """
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()
        role = (data.get("role") or data.get("status") or "student").strip().lower()
        password = data.get("password") or ""

        if not name or not email:
            return {"success": False, "user": None, "error": "Name and email are required"}

        if role not in VALID_ROLES:
            return {"success": False, "user": None, "error": f"Invalid role '{role}'"}

        existing = User.query.filter_by(email=email).first()
        if existing:
            return {"success": False, "user": None, "error": f"Email '{email}' is already registered in the database"}

        password_hash = generate_password_hash(password) if password else None

        try:
            user = User.create({
                "name": name,
                "email": email,
                "role": role,
                "status": role,
                "department": (data.get("department") or "").strip() or None,
                "graduation_year": data.get("graduation_year"),
                "password_hash": password_hash,
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
        role = (data.get("role") or data.get("status") or "student").strip().lower()

        if not name or not email:
            return {"success": False, "user": None, "error": "Name and email are required"}

        if role not in VALID_ROLES:
            return {"success": False, "user": None, "error": f"Invalid role '{role}'"}

        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user_id:
            return {"success": False, "user": None, "error": f"Email '{email}' is already in use by another user"}

        try:
            user = User.update(user_id, {
                "name": name,
                "email": email,
                "role": role,
                "status": role,
                "department": (data.get("department") or "").strip() or None,
                "graduation_year": data.get("graduation_year"),
                "password": data.get("password"),
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
