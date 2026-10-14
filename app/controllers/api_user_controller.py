"""
ApiUserController — JSON API controller with database connection.

Handles /api/users routes and returns structured JSON responses
with HTTP status codes. Delegates all data operations to the SQLAlchemy User model.
"""

from flask import request, jsonify
from app.models.user import User


class ApiUserController:

    # ------------------------------------------------------------------
    # CREATE — POST /api/users
    # ------------------------------------------------------------------

    @staticmethod
    def create():
        """
        Create a new user from JSON body or form-data with database uniqueness validation.
        """
        data = request.form.to_dict() if request.form else request.get_json() or {}

        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()

        if not name or not email:
            return jsonify({
                "status": "error",
                "message": "name and email are required"
            }), 400

        # Database conflict check
        if User.query.filter_by(email=email).first():
            return jsonify({
                "status": "error",
                "message": f"Email '{email}' is already registered in the database"
            }), 409

        try:
            user = User.create({
                "name": name,
                "email": email,
                "status": data.get("status", "student"),
                "department": data.get("department"),
                "graduation_year": data.get("graduation_year"),
            })
            return jsonify({
                "status": "success",
                "user": user.to_dict()
            }), 201
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}"
            }), 500

    # ------------------------------------------------------------------
    # READ ALL — GET /api/users
    # ------------------------------------------------------------------

    @staticmethod
    def index():
        """
        Return all users from the database.
        """
        try:
            return jsonify({
                "status": "success",
                "count": User.query.count(),
                "users": User.get_all()
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}"
            }), 500

    # ------------------------------------------------------------------
    # READ ONE — GET /api/users/<id>
    # ------------------------------------------------------------------

    @staticmethod
    def show(user_id: int):
        """
        Return a single user by ID from the database.
        """
        try:
            user = User.get_by_id(user_id)
            if user is None:
                return jsonify({
                    "status": "error",
                    "message": f"User {user_id} not found"
                }), 404
            return jsonify({
                "status": "success",
                "user": user.to_dict()
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}"
            }), 500

    # ------------------------------------------------------------------
    # UPDATE (full replace) — PUT /api/users/<id>
    # ------------------------------------------------------------------

    @staticmethod
    def update(user_id: int):
        """
        Fully replace a user's fields in the database.
        """
        data = request.form.to_dict() if request.form else request.get_json() or {}

        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()

        if not name or not email:
            return jsonify({
                "status": "error",
                "message": "name and email are required"
            }), 400

        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user_id:
            return jsonify({
                "status": "error",
                "message": f"Email '{email}' is already in use by another user"
            }), 409

        try:
            user = User.update(user_id, {
                "name": name,
                "email": email,
                "status": data.get("status", "student"),
                "department": data.get("department"),
                "graduation_year": data.get("graduation_year"),
            })
            if user is None:
                return jsonify({
                    "status": "error",
                    "message": f"User {user_id} not found"
                }), 404
            return jsonify({
                "status": "success",
                "user": user.to_dict()
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}"
            }), 500

    # ------------------------------------------------------------------
    # PARTIAL UPDATE — PATCH /api/users/<id>
    # ------------------------------------------------------------------

    @staticmethod
    def partial_update(user_id: int):
        """
        Update only the fields provided in the request body.
        """
        data = request.form.to_dict() if request.form else request.get_json() or {}

        email = data.get("email")
        if email:
            email = email.strip().lower()
            existing = User.query.filter_by(email=email).first()
            if existing and existing.id != user_id:
                return jsonify({
                    "status": "error",
                    "message": f"Email '{email}' is already in use by another user"
                }), 409
            data["email"] = email

        try:
            user = User.partial_update(user_id, data)
            if user is None:
                return jsonify({
                    "status": "error",
                    "message": f"User {user_id} not found"
                }), 404
            return jsonify({
                "status": "success",
                "user": user.to_dict()
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}"
            }), 500

    # ------------------------------------------------------------------
    # DELETE — DELETE /api/users/<id>
    # ------------------------------------------------------------------

    @staticmethod
    def delete(user_id: int):
        """
        Delete a user by ID from the database.
        """
        try:
            deleted = User.delete(user_id)
            if not deleted:
                return jsonify({
                    "status": "error",
                    "message": f"User {user_id} not found"
                }), 404
            return jsonify({
                "status": "success",
                "message": f"User {user_id} deleted"
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}"
            }), 500
