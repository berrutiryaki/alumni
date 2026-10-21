"""
API JobPosting routes — JSON responses.
Blueprint prefix: /api/job-postings
Delegates to: ApiJobPostingController
"""

from flask import Blueprint
from app.controllers.api_job_posting_controller import ApiJobPostingController

api_job_postings_bp = Blueprint("api_job_postings", __name__, url_prefix="/api/job-postings")


@api_job_postings_bp.route("/", methods=["GET"], strict_slashes=False)
@api_job_postings_bp.route("", methods=["GET"])
def index():
    """
    Get all job postings.
    ---
    tags:
      - Job Postings
    responses:
      200:
        description: List of all job postings
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            count:
              type: integer
              example: 5
            job_postings:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  description:
                    type: string
                  company:
                    type: string
                  location:
                    type: string
                  employment_type:
                    type: string
                  salary_range:
                    type: string
                  posted_by:
                    type: string
                  is_active:
                    type: boolean
                  created_at:
                    type: string
                  expires_at:
                    type: string
                  user_id:
                    type: integer
    """
    return ApiJobPostingController.index()


@api_job_postings_bp.route("/", methods=["POST"], strict_slashes=False)
@api_job_postings_bp.route("", methods=["POST"])
def create():
    """
    Create a new job posting.
    ---
    tags:
      - Job Postings
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: title
        in: formData
        type: string
        required: true
        description: Job title
      - name: description
        in: formData
        type: string
        required: true
        description: Detailed job description
      - name: company
        in: formData
        type: string
        required: true
        description: Hiring company name
      - name: location
        in: formData
        type: string
        description: Job location (e.g. Remote, Istanbul)
      - name: employment_type
        in: formData
        type: string
        description: "Employment type: full-time, part-time, internship, contract, remote"
      - name: salary_range
        in: formData
        type: string
        description: Salary information
      - name: posted_by
        in: formData
        type: string
        description: Publisher name or contact
      - name: is_active
        in: formData
        type: boolean
        description: Whether posting is active
      - name: expires_at
        in: formData
        type: string
        description: Expiration date (YYYY-MM-DD)
      - name: user_id
        in: formData
        type: integer
        description: ID of user who published the post
    responses:
      201:
        description: Job posting created
      400:
        description: Missing required fields (title, description, company)
    """
    return ApiJobPostingController.create()


@api_job_postings_bp.route("/<int:job_posting_id>", methods=["GET"])
def show(job_posting_id):
    """
    Get a job posting by ID.
    ---
    tags:
      - Job Postings
    parameters:
      - name: job_posting_id
        in: path
        type: integer
        required: true
        description: Job posting ID
    responses:
      200:
        description: Job posting found
      404:
        description: Job posting not found
    """
    return ApiJobPostingController.show(job_posting_id)


@api_job_postings_bp.route("/<int:job_posting_id>", methods=["PUT"])
def update(job_posting_id):
    """
    Fully replace a job posting by ID.
    ---
    tags:
      - Job Postings
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: job_posting_id
        in: path
        type: integer
        required: true
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
      - name: user_id
        in: formData
        type: integer
    responses:
      200:
        description: Job posting updated
      400:
        description: Missing required fields
      404:
        description: Job posting not found
    """
    return ApiJobPostingController.update(job_posting_id)


@api_job_postings_bp.route("/<int:job_posting_id>", methods=["PATCH"])
def partial_update(job_posting_id):
    """
    Partially update a job posting by ID.
    ---
    tags:
      - Job Postings
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: job_posting_id
        in: path
        type: integer
        required: true
      - name: title
        in: formData
        type: string
      - name: description
        in: formData
        type: string
      - name: company
        in: formData
        type: string
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
      - name: user_id
        in: formData
        type: integer
    responses:
      200:
        description: Job posting partially updated
      404:
        description: Job posting not found
    """
    return ApiJobPostingController.partial_update(job_posting_id)


@api_job_postings_bp.route("/<int:job_posting_id>", methods=["DELETE"])
def delete(job_posting_id):
    """
    Delete a job posting by ID.
    ---
    tags:
      - Job Postings
    parameters:
      - name: job_posting_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Job posting deleted
      404:
        description: Job posting not found
    """
    return ApiJobPostingController.delete(job_posting_id)
