"""
API Application routes — JSON responses.
Blueprint prefix: /api/applications
Delegates to: ApiApplicationController
"""

from flask import Blueprint
from app.controllers.api_application_controller import ApiApplicationController

api_applications_bp = Blueprint("api_applications", __name__, url_prefix="/api/applications")


@api_applications_bp.route("/", methods=["GET"], strict_slashes=False)
@api_applications_bp.route("", methods=["GET"])
def index():
    """
    Get all job applications.
    ---
    tags:
      - Applications
    responses:
      200:
        description: List of all applications
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            count:
              type: integer
              example: 10
            applications:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  user_id:
                    type: integer
                  job_posting_id:
                    type: integer
                  resume_url:
                    type: string
                  cover_letter:
                    type: string
                  status:
                    type: string
                  applied_at:
                    type: string
                  user_name:
                    type: string
                  job_title:
                    type: string
                  company:
                    type: string
    """
    return ApiApplicationController.index()


@api_applications_bp.route("/", methods=["POST"], strict_slashes=False)
@api_applications_bp.route("", methods=["POST"])
def create():
    """
    Submit a new job application.
    ---
    tags:
      - Applications
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: user_id
        in: formData
        type: integer
        required: true
        description: Applicant user ID
      - name: job_posting_id
        in: formData
        type: integer
        required: true
        description: Targeted job posting ID
      - name: resume_url
        in: formData
        type: string
        description: CV / LinkedIn / portfolio URL
      - name: cover_letter
        in: formData
        type: string
        description: Motivation or cover letter
      - name: status
        in: formData
        type: string
        description: "Application status: pending, reviewed, accepted, rejected"
    responses:
      201:
        description: Application created
      400:
        description: Missing required fields or invalid integer IDs
      404:
        description: User or Job Posting not found
    """
    return ApiApplicationController.create()


@api_applications_bp.route("/<int:application_id>", methods=["GET"])
def show(application_id):
    """
    Get an application by ID.
    ---
    tags:
      - Applications
    parameters:
      - name: application_id
        in: path
        type: integer
        required: true
        description: Application ID
    responses:
      200:
        description: Application found
      404:
        description: Application not found
    """
    return ApiApplicationController.show(application_id)


@api_applications_bp.route("/<int:application_id>", methods=["PUT"])
def update(application_id):
    """
    Fully replace an application by ID.
    ---
    tags:
      - Applications
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: application_id
        in: path
        type: integer
        required: true
      - name: user_id
        in: formData
        type: integer
        required: true
      - name: job_posting_id
        in: formData
        type: integer
        required: true
      - name: resume_url
        in: formData
        type: string
      - name: cover_letter
        in: formData
        type: string
      - name: status
        in: formData
        type: string
    responses:
      200:
        description: Application updated
      400:
        description: Missing required fields
      404:
        description: Application, User, or Job Posting not found
    """
    return ApiApplicationController.update(application_id)


@api_applications_bp.route("/<int:application_id>", methods=["PATCH"])
def partial_update(application_id):
    """
    Partially update an application by ID.
    ---
    tags:
      - Applications
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: application_id
        in: path
        type: integer
        required: true
      - name: user_id
        in: formData
        type: integer
      - name: job_posting_id
        in: formData
        type: integer
      - name: resume_url
        in: formData
        type: string
      - name: cover_letter
        in: formData
        type: string
      - name: status
        in: formData
        type: string
    responses:
      200:
        description: Application partially updated
      404:
        description: Application not found
    """
    return ApiApplicationController.partial_update(application_id)


@api_applications_bp.route("/<int:application_id>", methods=["DELETE"])
def delete(application_id):
    """
    Delete an application by ID.
    ---
    tags:
      - Applications
    parameters:
      - name: application_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Application deleted
      404:
        description: Application not found
    """
    return ApiApplicationController.delete(application_id)
