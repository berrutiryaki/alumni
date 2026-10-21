"""
ApplicationController — HTML / web-facing controller with database connection.

Delegates all data operations to the SQLAlchemy Application model.
Returns plain dicts consumed by the web route layer.
"""

from app.models.application import Application
from app.models.user import User
from app.models.job_posting import JobPosting


class ApplicationController:

    @staticmethod
    def index() -> dict:
        try:
            return {"success": True, "applications": Application.get_all()}
        except Exception as e:
            return {"success": False, "applications": [], "error": f"Database error: {str(e)}"}

    @staticmethod
    def show(application_id: int) -> dict:
        try:
            app_rec = Application.get_by_id(application_id)
            if app_rec is None:
                return {"success": False, "application": None, "error": f"Application {application_id} not found"}
            return {"success": True, "application": app_rec.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "application": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def create(data: dict) -> dict:
        user_id = data.get("user_id")
        job_posting_id = data.get("job_posting_id")

        if not user_id or not job_posting_id:
            return {"success": False, "application": None, "error": "user_id and job_posting_id are required"}

        try:
            user = User.get_by_id(int(user_id))
            job = JobPosting.get_by_id(int(job_posting_id))
            if not user:
                return {"success": False, "application": None, "error": f"User {user_id} does not exist"}
            if not job:
                return {"success": False, "application": None, "error": f"Job Posting {job_posting_id} does not exist"}

            app_rec = Application.create({
                "user_id": int(user_id),
                "job_posting_id": int(job_posting_id),
                "resume_url": (data.get("resume_url") or "").strip() or None,
                "cover_letter": (data.get("cover_letter") or "").strip() or None,
                "status": (data.get("status") or "").strip() or "pending",
            })
            return {"success": True, "application": app_rec.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "application": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def update(application_id: int, data: dict) -> dict:
        user_id = data.get("user_id")
        job_posting_id = data.get("job_posting_id")

        if not user_id or not job_posting_id:
            return {"success": False, "application": None, "error": "user_id and job_posting_id are required"}

        try:
            user = User.get_by_id(int(user_id))
            job = JobPosting.get_by_id(int(job_posting_id))
            if not user:
                return {"success": False, "application": None, "error": f"User {user_id} does not exist"}
            if not job:
                return {"success": False, "application": None, "error": f"Job Posting {job_posting_id} does not exist"}

            app_rec = Application.update(application_id, {
                "user_id": int(user_id),
                "job_posting_id": int(job_posting_id),
                "resume_url": (data.get("resume_url") or "").strip() or None,
                "cover_letter": (data.get("cover_letter") or "").strip() or None,
                "status": (data.get("status") or "").strip() or "pending",
            })
            if app_rec is None:
                return {"success": False, "application": None, "error": f"Application {application_id} not found"}
            return {"success": True, "application": app_rec.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "application": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def delete(application_id: int) -> dict:
        try:
            deleted = Application.delete(application_id)
            if not deleted:
                return {"success": False, "message": f"Application {application_id} not found"}
            return {"success": True, "message": f"Application {application_id} deleted successfully"}
        except Exception as e:
            return {"success": False, "message": f"Database error: {str(e)}"}
