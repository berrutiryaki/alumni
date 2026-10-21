"""
JobPostingController — HTML / web-facing controller with database connection.

Delegates all data operations to the SQLAlchemy JobPosting model.
Returns plain dicts consumed by the web route layer.
"""

from app.models.job_posting import JobPosting


class JobPostingController:

    @staticmethod
    def index() -> dict:
        try:
            return {"success": True, "job_postings": JobPosting.get_all()}
        except Exception as e:
            return {"success": False, "job_postings": [], "error": f"Database error: {str(e)}"}

    @staticmethod
    def show(job_posting_id: int) -> dict:
        try:
            jp = JobPosting.get_by_id(job_posting_id)
            if jp is None:
                return {"success": False, "job_posting": None, "error": f"Job posting {job_posting_id} not found"}
            return {"success": True, "job_posting": jp.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "job_posting": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def create(data: dict) -> dict:
        title = (data.get("title") or "").strip()
        description = (data.get("description") or "").strip()
        company = (data.get("company") or "").strip()

        if not title or not description or not company:
            return {"success": False, "job_posting": None, "error": "Title, description, and company are required"}

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
            })
            return {"success": True, "job_posting": jp.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "job_posting": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def update(job_posting_id: int, data: dict) -> dict:
        title = (data.get("title") or "").strip()
        description = (data.get("description") or "").strip()
        company = (data.get("company") or "").strip()

        if not title or not description or not company:
            return {"success": False, "job_posting": None, "error": "Title, description, and company are required"}

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
            })
            if jp is None:
                return {"success": False, "job_posting": None, "error": f"Job posting {job_posting_id} not found"}
            return {"success": True, "job_posting": jp.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "job_posting": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def partial_update(job_posting_id: int, data: dict) -> dict:
        try:
            jp = JobPosting.partial_update(job_posting_id, data)
            if jp is None:
                return {"success": False, "job_posting": None, "error": f"Job posting {job_posting_id} not found"}
            return {"success": True, "job_posting": jp.to_dict(), "error": None}
        except Exception as e:
            return {"success": False, "job_posting": None, "error": f"Database error: {str(e)}"}

    @staticmethod
    def delete(job_posting_id: int) -> dict:
        try:
            deleted = JobPosting.delete(job_posting_id)
            if not deleted:
                return {"success": False, "message": f"Job posting {job_posting_id} not found"}
            return {"success": True, "message": f"Job posting {job_posting_id} deleted successfully"}
        except Exception as e:
            return {"success": False, "message": f"Database error: {str(e)}"}
