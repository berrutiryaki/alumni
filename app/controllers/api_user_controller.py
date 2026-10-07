"""
ApiUserController — JSON API controller.

Handles /api/users routes and returns structured JSON responses
with HTTP status codes. Delegates all data operations to the User model.
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
        Create a new user from JSON body or form-data.

        Expected fields: name (required), email (required),
                         department (optional), graduation_year (optional)

        Returns:
            201 Created  — user created successfully
            400 Bad Request — missing required fields
        """
        data = request.form.to_dict() if request.form else request.get_json() or {}

        if not data.get("name") or not data.get("email"):
            return jsonify({
                "status": "error",
                "message": "name and email are required"
            }), 400

        user = User.create(data)
        return jsonify({
            "status": "success",
            "user": user.to_dict()
        }), 201

    # ------------------------------------------------------------------
    # READ ALL — GET /api/users
    # ------------------------------------------------------------------

    @staticmethod
    def index():
        """
        Return all users.

        Returns:
            200 OK — list of all users
        """
        return jsonify({
            "status": "success",
            "users": User.get_all()
        }), 200

    # ------------------------------------------------------------------
    # READ ONE — GET /api/users/<id>
    # ------------------------------------------------------------------

    @staticmethod
    def show(user_id: int):
        """
        Return a single user by ID.

        Returns:
            200 OK        — user found
            404 Not Found — user does not exist
        """
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

    # ------------------------------------------------------------------
    # UPDATE (full replace) — PUT /api/users/<id>
    # ------------------------------------------------------------------

    @staticmethod
    def update(user_id: int):
        """
        Fully replace a user's fields.

        Returns:
            200 OK        — user updated
            400 Bad Request — missing required fields
            404 Not Found — user does not exist
        """
        data = request.form.to_dict() if request.form else request.get_json() or {}

        if not data.get("name") or not data.get("email"):
            return jsonify({
                "status": "error",
                "message": "name and email are required"
            }), 400

        user = User.update(user_id, data)
        if user is None:
            return jsonify({
                "status": "error",
                "message": f"User {user_id} not found"
            }), 404
        return jsonify({
            "status": "success",
            "user": user.to_dict()
        }), 200

    # ------------------------------------------------------------------
    # PARTIAL UPDATE — PATCH /api/users/<id>
    # ------------------------------------------------------------------

    @staticmethod
    def partial_update(user_id: int):
        """
        Update only the fields provided in the request body.

        Returns:
            200 OK        — user partially updated
            404 Not Found — user does not exist
        """
        data = request.form.to_dict() if request.form else request.get_json() or {}

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

    # ------------------------------------------------------------------
    # DELETE — DELETE /api/users/<id>
    # ------------------------------------------------------------------

    @staticmethod
    def delete(user_id: int):
        """
        Delete a user by ID.

        Returns:
            200 OK        — user deleted
            404 Not Found — user does not exist
        """
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
