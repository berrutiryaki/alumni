"""
API User routes — JSON responses.
Blueprint prefix: /api/users
Delegates to: ApiUserController
"""

from flask import Blueprint
from app.controllers.api_user_controller import ApiUserController

api_users_bp = Blueprint("api_users", __name__, url_prefix="/api/users")


@api_users_bp.route("/", methods=["GET"])
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


@api_users_bp.route("/", methods=["POST"])
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
