"""
ApiApplicationController — JSON API controller with database connection.

Handles /api/applications routes and returns structured JSON responses.
Delegates all data operations to the SQLAlchemy Application model.
Supports nested filtering by user_id and job_posting_id.
"""

from flask import request, jsonify
from app.models.application import Application
from app.models.user import User
from app.models.job_posting import JobPosting


class ApiApplicationController:

    @staticmethod
    def index():
        try:
            return jsonify({
                "status": "success",
                "count": Application.query.count(),
                "applications": Application.get_all()
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def show(application_id: int):
        try:
            app_rec = Application.get_by_id(application_id)
            if app_rec is None:
                return jsonify({"status": "error", "message": f"Application {application_id} not found"}), 404
            return jsonify({"status": "success", "application": app_rec.to_dict()}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def create(extra_data: dict = None):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        if extra_data:
            data.update(extra_data)

        user_id = data.get("user_id")
        job_posting_id = data.get("job_posting_id")

        if not user_id or not job_posting_id:
            return jsonify({"status": "error", "message": "user_id and job_posting_id are required"}), 400

        try:
            user = User.get_by_id(int(user_id))
            job = JobPosting.get_by_id(int(job_posting_id))
            if not user:
                return jsonify({"status": "error", "message": f"User {user_id} not found"}), 404
            if not job:
                return jsonify({"status": "error", "message": f"Job posting {job_posting_id} not found"}), 404

            app_rec = Application.create({
                "user_id": int(user_id),
                "job_posting_id": int(job_posting_id),
                "resume_url": (data.get("resume_url") or "").strip() or None,
                "cover_letter": (data.get("cover_letter") or "").strip() or None,
                "status": (data.get("status") or "").strip() or "pending",
            })
            return jsonify({"status": "success", "application": app_rec.to_dict()}), 201
        except ValueError:
            return jsonify({"status": "error", "message": "user_id and job_posting_id must be valid integers"}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def update(application_id: int):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        user_id = data.get("user_id")
        job_posting_id = data.get("job_posting_id")

        if not user_id or not job_posting_id:
            return jsonify({"status": "error", "message": "user_id and job_posting_id are required"}), 400

        try:
            user = User.get_by_id(int(user_id))
            job = JobPosting.get_by_id(int(job_posting_id))
            if not user:
                return jsonify({"status": "error", "message": f"User {user_id} not found"}), 404
            if not job:
                return jsonify({"status": "error", "message": f"Job posting {job_posting_id} not found"}), 404

            app_rec = Application.update(application_id, {
                "user_id": int(user_id),
                "job_posting_id": int(job_posting_id),
                "resume_url": (data.get("resume_url") or "").strip() or None,
                "cover_letter": (data.get("cover_letter") or "").strip() or None,
                "status": (data.get("status") or "").strip() or "pending",
            })
            if app_rec is None:
                return jsonify({"status": "error", "message": f"Application {application_id} not found"}), 404
            return jsonify({"status": "success", "application": app_rec.to_dict()}), 200
        except ValueError:
            return jsonify({"status": "error", "message": "user_id and job_posting_id must be valid integers"}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def partial_update(application_id: int):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        try:
            if "user_id" in data:
                user = User.get_by_id(int(data["user_id"]))
                if not user:
                    return jsonify({"status": "error", "message": f"User {data['user_id']} not found"}), 404
            if "job_posting_id" in data:
                job = JobPosting.get_by_id(int(data["job_posting_id"]))
                if not job:
                    return jsonify({"status": "error", "message": f"Job posting {data['job_posting_id']} not found"}), 404

            app_rec = Application.partial_update(application_id, data)
            if app_rec is None:
                return jsonify({"status": "error", "message": f"Application {application_id} not found"}), 404
            return jsonify({"status": "success", "application": app_rec.to_dict()}), 200
        except ValueError:
            return jsonify({"status": "error", "message": "ID values must be valid integers"}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def delete(application_id: int):
        try:
            deleted = Application.delete(application_id)
            if not deleted:
                return jsonify({"status": "error", "message": f"Application {application_id} not found"}), 404
            return jsonify({"status": "success", "message": f"Application {application_id} deleted"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    # ------------------------------------------------------------------
    # Nested: filter by user_id
    # ------------------------------------------------------------------

    @staticmethod
    def index_by_user(user_id: int):
        """Return all applications submitted by a specific user."""
        try:
            user = User.get_by_id(user_id)
            if user is None:
                return jsonify({"status": "error", "message": f"User {user_id} not found"}), 404
            apps = Application.query.filter_by(user_id=user_id).order_by(Application.id.asc()).all()
            return jsonify({
                "status": "success",
                "count": len(apps),
                "user_id": user_id,
                "applications": [a.to_dict() for a in apps]
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    # ------------------------------------------------------------------
    # Nested: filter by job_posting_id
    # ------------------------------------------------------------------

    @staticmethod
    def index_by_job_posting(job_posting_id: int):
        """Return all applications received for a specific job posting."""
        try:
            job = JobPosting.get_by_id(job_posting_id)
            if job is None:
                return jsonify({"status": "error", "message": f"Job posting {job_posting_id} not found"}), 404
            apps = Application.query.filter_by(job_posting_id=job_posting_id).order_by(Application.id.asc()).all()
            return jsonify({
                "status": "success",
                "count": len(apps),
                "job_posting_id": job_posting_id,
                "applications": [a.to_dict() for a in apps]
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
