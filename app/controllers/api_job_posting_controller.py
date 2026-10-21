"""
ApiJobPostingController — JSON API controller with database connection.

Handles /api/job-postings routes and returns structured JSON responses.
Delegates all data operations to the SQLAlchemy JobPosting model.
"""

from flask import request, jsonify
from app.models.job_posting import JobPosting


class ApiJobPostingController:

    @staticmethod
    def index():
        try:
            return jsonify({
                "status": "success",
                "count": JobPosting.query.count(),
                "job_postings": JobPosting.get_all()
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def show(job_posting_id: int):
        try:
            jp = JobPosting.get_by_id(job_posting_id)
            if jp is None:
                return jsonify({"status": "error", "message": f"Job posting {job_posting_id} not found"}), 404
            return jsonify({"status": "success", "job_posting": jp.to_dict()}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def create(extra_data: dict = None):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        if extra_data:
            data.update(extra_data)

        title = (data.get("title") or "").strip()
        description = (data.get("description") or "").strip()
        company = (data.get("company") or "").strip()

        if not title or not description or not company:
            return jsonify({"status": "error", "message": "title, description, and company are required"}), 400

        try:
            jp = JobPosting.create({
                "title": title,
                "description": description,
                "company": company,
                "location": (data.get("location") or "").strip() or None,
                "employment_type": (data.get("employment_type") or "").strip() or "full-time",
                "salary_range": (data.get("salary_range") or "").strip() or None,
                "posted_by": (data.get("posted_by") or "").strip() or None,
                "is_active": data.get("is_active", True) not in [False, "false", "0", 0],
                "expires_at": (data.get("expires_at") or "").strip() or None,
                "user_id": data.get("user_id"),
            })
            return jsonify({"status": "success", "job_posting": jp.to_dict()}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def update(job_posting_id: int):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        title = (data.get("title") or "").strip()
        description = (data.get("description") or "").strip()
        company = (data.get("company") or "").strip()

        if not title or not description or not company:
            return jsonify({"status": "error", "message": "title, description, and company are required"}), 400

        try:
            jp = JobPosting.update(job_posting_id, {
                "title": title,
                "description": description,
                "company": company,
                "location": (data.get("location") or "").strip() or None,
                "employment_type": (data.get("employment_type") or "").strip() or "full-time",
                "salary_range": (data.get("salary_range") or "").strip() or None,
                "posted_by": (data.get("posted_by") or "").strip() or None,
                "is_active": data.get("is_active", True) not in [False, "false", "0", 0],
                "expires_at": (data.get("expires_at") or "").strip() or None,
                "user_id": data.get("user_id"),
            })
            if jp is None:
                return jsonify({"status": "error", "message": f"Job posting {job_posting_id} not found"}), 404
            return jsonify({"status": "success", "job_posting": jp.to_dict()}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def partial_update(job_posting_id: int):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        try:
            jp = JobPosting.partial_update(job_posting_id, data)
            if jp is None:
                return jsonify({"status": "error", "message": f"Job posting {job_posting_id} not found"}), 404
            return jsonify({"status": "success", "job_posting": jp.to_dict()}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def delete(job_posting_id: int):
        try:
            deleted = JobPosting.delete(job_posting_id)
            if not deleted:
                return jsonify({"status": "error", "message": f"Job posting {job_posting_id} not found"}), 404
            return jsonify({"status": "success", "message": f"Job posting {job_posting_id} deleted"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    # ------------------------------------------------------------------
    # Nested: filter by user_id
    # ------------------------------------------------------------------

    @staticmethod
    def index_by_user(user_id: int):
        """Return all job postings belonging to a specific user."""
        try:
            from app.models.user import User
            user = User.get_by_id(user_id)
            if user is None:
                return jsonify({"status": "error", "message": f"User {user_id} not found"}), 404
            job_postings = JobPosting.query.filter_by(user_id=user_id).order_by(JobPosting.id.asc()).all()
            return jsonify({
                "status": "success",
                "count": len(job_postings),
                "user_id": user_id,
                "job_postings": [jp.to_dict() for jp in job_postings]
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
