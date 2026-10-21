"""
API User routes — JSON responses.
Blueprint prefix: /api/users
Delegates to: ApiUserController
"""

from flask import Blueprint
from app.controllers.api_user_controller import ApiUserController
from app.controllers.api_announcement_controller import ApiAnnouncementController
from app.controllers.api_job_posting_controller import ApiJobPostingController

api_users_bp = Blueprint("api_users", __name__, url_prefix="/api/users")


@api_users_bp.route("/", methods=["GET"], strict_slashes=False)
@api_users_bp.route("", methods=["GET"])
def index():
    """
    Get all users.
    ---
    tags:
      - Users
    responses:
      200:
        description: List of all users
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            users:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
                  department:
                    type: string
                  graduation_year:
                    type: integer
    """
    return ApiUserController.index()


@api_users_bp.route("/", methods=["POST"], strict_slashes=False)
@api_users_bp.route("", methods=["POST"])
def create():
    """
    Create a new user.
    ---
    tags:
      - Users
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Full name
      - name: email
        in: formData
        type: string
        required: true
        description: Email address
      - name: department
        in: formData
        type: string
        description: Academic department
      - name: graduation_year
        in: formData
        type: integer
        description: Year of graduation
    responses:
      201:
        description: User created
      400:
        description: Missing required fields
    """
    return ApiUserController.create()


@api_users_bp.route("/<int:user_id>", methods=["GET"])
def show(user_id):
    """
    Get a user by ID.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User found
      404:
        description: User not found
    """
    return ApiUserController.show(user_id)


@api_users_bp.route("/<int:user_id>", methods=["PUT"])
def update(user_id):
    """
    Fully replace a user by ID.
    ---
    tags:
      - Users
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: name
        in: formData
        type: string
        required: true
      - name: email
        in: formData
        type: string
        required: true
      - name: department
        in: formData
        type: string
      - name: graduation_year
        in: formData
        type: integer
    responses:
      200:
        description: User updated
      400:
        description: Missing required fields
      404:
        description: User not found
    """
    return ApiUserController.update(user_id)


@api_users_bp.route("/<int:user_id>", methods=["PATCH"])
def partial_update(user_id):
    """
    Partially update a user by ID.
    ---
    tags:
      - Users
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: name
        in: formData
        type: string
      - name: email
        in: formData
        type: string
      - name: department
        in: formData
        type: string
      - name: graduation_year
        in: formData
        type: integer
    responses:
      200:
        description: User partially updated
      404:
        description: User not found
    """
    return ApiUserController.partial_update(user_id)


@api_users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    """
    Delete a user by ID.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: User deleted
      404:
        description: User not found
    """
    return ApiUserController.delete(user_id)


# ------------------------------------------------------------------
# Nested Routes: User's Announcements & Job Postings
# ------------------------------------------------------------------

@api_users_bp.route("/<int:user_id>/announcements", methods=["GET"])
def user_announcements(user_id):
    """
    Get all announcements authored by a specific user (nested route).
    ---
    tags:
      - Users (Nested)
      - Announcements
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the author user
    responses:
      200:
        description: List of announcements for the user
      404:
        description: User not found
    """
    return ApiAnnouncementController.index_by_user(user_id)


@api_users_bp.route("/<int:user_id>/announcements", methods=["POST"])
def create_user_announcement(user_id):
    """
    Create an announcement directly under a user (nested route).
    ---
    tags:
      - Users (Nested)
      - Announcements
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the author user
      - name: title
        in: formData
        type: string
        required: true
      - name: content
        in: formData
        type: string
        required: true
      - name: author
        in: formData
        type: string
      - name: is_active
        in: formData
        type: boolean
    responses:
      201:
        description: Announcement created for user
      400:
        description: Missing required fields
      404:
        description: User not found
    """
    from app.models.user import User
    from flask import jsonify
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"status": "error", "message": f"User {user_id} not found"}), 404
    return ApiAnnouncementController.create(extra_data={"user_id": user_id})


@api_users_bp.route("/<int:user_id>/job-postings", methods=["GET"])
def user_job_postings(user_id):
    """
    Get all job postings published by a specific user (nested route).
    ---
    tags:
      - Users (Nested)
      - Job Postings
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the publisher user
    responses:
      200:
        description: List of job postings for the user
      404:
        description: User not found
    """
    return ApiJobPostingController.index_by_user(user_id)


@api_users_bp.route("/<int:user_id>/job-postings", methods=["POST"])
def create_user_job_posting(user_id):
    """
    Create a job posting directly under a user (nested route).
    ---
    tags:
      - Users (Nested)
      - Job Postings
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the publisher user
      - name: title
        in: formData
        type: string
        required: true
      - name: description
        in: formData
        type: string
        required: true
      - name: company
        in: formData
        type: string
        required: true
      - name: location
        in: formData
        type: string
      - name: employment_type
        in: formData
        type: string
      - name: salary_range
        in: formData
        type: string
      - name: posted_by
        in: formData
        type: string
      - name: is_active
        in: formData
        type: boolean
      - name: expires_at
        in: formData
        type: string
    responses:
      201:
        description: Job posting created for user
      400:
        description: Missing required fields
      404:
        description: User not found
    """
    from app.models.user import User
    from flask import jsonify
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"status": "error", "message": f"User {user_id} not found"}), 404
    return ApiJobPostingController.create(extra_data={"user_id": user_id})

