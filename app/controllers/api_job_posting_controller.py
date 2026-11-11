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
    def create():
        data = request.form.to_dict() if request.form else request.get_json() or {}

        title = (data.get("title") or "").strip()
        company = (data.get("company") or "").strip()
        employment_type = (data.get("employment_type") or "").strip()
        salary_range = (data.get("salary_range") or "").strip()
        city = (data.get("city") or data.get("location") or "").strip() or None
        description = (data.get("description") or "").strip() or None

        if not title or not company or not employment_type or not salary_range:
            return jsonify({
                "status": "error",
                "message": "title, company, employment_type, and salary_range are required"
            }), 400

        if len(title) > 120 or len(company) > 120 or (city and len(city) > 120):
            return jsonify({
                "status": "error",
                "message": "title, company, and city must not exceed 120 characters"
            }), 400

        try:
            jp = JobPosting.create({
                "title": title,
                "company": company,
                "city": city,
                "description": description,
                "employment_type": employment_type,
                "salary_range": salary_range,
                "posted_by": (data.get("posted_by") or "").strip() or None,
                "is_active": data.get("is_active", True) not in [False, "false", "0", 0],
                "expires_at": (data.get("expires_at") or "").strip() or None,
            })
            return jsonify({"status": "success", "job_posting": jp.to_dict()}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

    @staticmethod
    def update(job_posting_id: int):
        data = request.form.to_dict() if request.form else request.get_json() or {}
        title = (data.get("title") or "").strip()
        company = (data.get("company") or "").strip()
        employment_type = (data.get("employment_type") or "").strip()
        salary_range = (data.get("salary_range") or "").strip()
        city = (data.get("city") or data.get("location") or "").strip() or None
        description = (data.get("description") or "").strip() or None

        if not title or not company or not employment_type or not salary_range:
            return jsonify({
                "status": "error",
                "message": "title, company, employment_type, and salary_range are required"
            }), 400

        if len(title) > 120 or len(company) > 120 or (city and len(city) > 120):
            return jsonify({
                "status": "error",
                "message": "title, company, and city must not exceed 120 characters"
            }), 400

        try:
            jp = JobPosting.update(job_posting_id, {
                "title": title,
                "company": company,
                "city": city,
                "description": description,
                "employment_type": employment_type,
                "salary_range": salary_range,
                "posted_by": (data.get("posted_by") or "").strip() or None,
                "is_active": data.get("is_active", True) not in [False, "false", "0", 0],
                "expires_at": (data.get("expires_at") or "").strip() or None,
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
