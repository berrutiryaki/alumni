"""
API Announcement routes — JSON responses.
Blueprint prefix: /api/announcements
Delegates to: ApiAnnouncementController
"""

from flask import Blueprint
from app.controllers.api_announcement_controller import ApiAnnouncementController

api_announcements_bp = Blueprint("api_announcements", __name__, url_prefix="/api/announcements")


@api_announcements_bp.route("/", methods=["GET"])
def index():
    """
    Get all announcements.
    ---
    tags:
      - Announcements
    responses:
      200:
        description: List of all announcements
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            announcements:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  content:
                    type: string
                  author:
                    type: string
                  is_active:
                    type: boolean
                  created_at:
                    type: string
    """
    return ApiAnnouncementController.index()


@api_announcements_bp.route("/", methods=["POST"])
def create():
    """
    Create a new announcement.
    ---
    tags:
      - Announcements
    consumes:
      - multipart/form-data
      - application/json
    parameters:
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
        description: Announcement created
      400:
        description: Missing required fields
    """
    return ApiAnnouncementController.create()


@api_announcements_bp.route("/<int:announcement_id>", methods=["GET"])
def show(announcement_id):
    """
    Get an announcement by ID.
    ---
    tags:
      - Announcements
    parameters:
      - name: announcement_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Announcement found
      404:
        description: Announcement not found
    """
    return ApiAnnouncementController.show(announcement_id)


@api_announcements_bp.route("/<int:announcement_id>", methods=["PUT"])
def update(announcement_id):
    """
    Fully replace an announcement by ID.
    ---
    tags:
      - Announcements
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: announcement_id
        in: path
        type: integer
        required: true
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
      200:
        description: Announcement updated
      400:
        description: Missing required fields
      404:
        description: Announcement not found
    """
    return ApiAnnouncementController.update(announcement_id)


@api_announcements_bp.route("/<int:announcement_id>", methods=["PATCH"])
def partial_update(announcement_id):
    """
    Partially update an announcement by ID.
    ---
    tags:
      - Announcements
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: announcement_id
        in: path
        type: integer
        required: true
      - name: title
        in: formData
        type: string
      - name: content
        in: formData
        type: string
      - name: author
        in: formData
        type: string
      - name: is_active
        in: formData
        type: boolean
    responses:
      200:
        description: Announcement partially updated
      404:
        description: Announcement not found
    """
    return ApiAnnouncementController.partial_update(announcement_id)


@api_announcements_bp.route("/<int:announcement_id>", methods=["DELETE"])
def delete(announcement_id):
    """
    Delete an announcement by ID.
    ---
    tags:
      - Announcements
    parameters:
      - name: announcement_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Announcement deleted
      404:
        description: Announcement not found
    """
    return ApiAnnouncementController.delete(announcement_id)
