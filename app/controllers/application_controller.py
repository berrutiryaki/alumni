"""
ApplicationController — HTML / web-facing controller with database connection.

Delegates all data operations to the SQLAlchemy Application model.
Enforces privacy filtering, duplicate prevention (409 Conflict),
auto-assigned user_id/pending status, and owner/admin status update permissions.
"""

from app.models.application import Application
from app.models.user import User
from app.models.job_posting import JobPosting

VALID_STATUSES = ("pending", "reviewed", "accepted", "rejected")


class ApplicationController:

    # ------------------------------------------------------------------
    # Authorization helpers
    # ------------------------------------------------------------------

    @staticmethod
    def is_job_owner(job_posting: JobPosting | None, user: User | None) -> bool:
        """Return True if job_posting.posted_by matches user.name or user.email."""
        if job_posting is None or user is None or not job_posting.posted_by:
            return False
        posted_by = job_posting.posted_by.strip().lower()
        user_name = (user.name or "").strip().lower()
        user_email = (user.email or "").strip().lower()
        return bool(posted_by and (posted_by == user_name or posted_by == user_email))

    @staticmethod
    def can_manage_application(app_rec: Application | None, user: User | None) -> bool:
        """Only admin or the owner of the target job posting can manage/update status."""
        if app_rec is None or user is None:
            return False
        if (user.role or "").strip().lower() == "admin":
            return True
        return ApplicationController.is_job_owner(app_rec.job_posting, user)

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    @staticmethod
    def index() -> dict:
        try:
            return {"success": True, "applications": Application.get_all()}
        except Exception as e:
            return {"success": False, "applications": [], "error": f"Database error: {str(e)}"}

    @staticmethod
    def index_for_user(user: User) -> dict:
        """
        Return privacy-filtered applications for the logged-in user:
          - admin: all applications
          - job posting owner (posted_by == user.name or user.email): applications to their postings
          - applicant (student / alumni): their own submitted applications (user_id == user.id)
        Each item includes `can_manage`, `is_own_application`, and `is_job_owner` flags.
        """
        try:
            role = (user.role or "student").strip().lower()
            all_records = Application.query.order_by(Application.id.desc()).all()

            visible = []
            for rec in all_records:
                owns_job = ApplicationController.is_job_owner(rec.job_posting, user)
                is_own = (rec.user_id == user.id)

                if role == "admin" or owns_job or is_own:
                    item = rec.to_dict()
                    item["can_manage"] = (role == "admin") or owns_job
                    item["is_job_owner"] = owns_job
                    item["is_own_application"] = is_own
                    visible.append(item)

            return {"success": True, "applications": visible, "error": None}
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

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    @staticmethod
    def create(data: dict, current_user: User | None = None) -> dict:
        """
        Create a new job application.
        - Always binds user_id to current_user.id when provided (never trusts form user_id).
        - Always forces status = 'pending'.
        - Blocks duplicate applications by the same user for the same job posting (409 Conflict).
        """
        user_id = current_user.id if current_user is not None else data.get("user_id")
        job_posting_id = data.get("job_posting_id")

        if not user_id or not job_posting_id:
            return {
                "success": False,
                "application": None,
                "error": "A valid applicant and job posting are required.",
                "status_code": 400,
            }

        try:
            uid = int(user_id)
            jid = int(job_posting_id)
        except (TypeError, ValueError):
            return {
                "success": False,
                "application": None,
                "error": "Invalid job posting identifier.",
                "status_code": 400,
            }

        try:
            user = User.get_by_id(uid)
            job = JobPosting.get_by_id(jid)
            if not user:
                return {
                    "success": False,
                    "application": None,
                    "error": f"User {uid} does not exist.",
                    "status_code": 404,
                }
            if not job:
                return {
                    "success": False,
                    "application": None,
                    "error": f"Job posting {jid} does not exist.",
                    "status_code": 404,
                }

            # Prevent duplicate application by the same user for the same job posting
            existing = Application.find_duplicate(uid, jid)
            if existing is not None:
                return {
                    "success": False,
                    "application": None,
                    "error": f"You have already submitted an application for '{job.title}' at {job.company}.",
                    "status_code": 409,
                }

            app_rec = Application.create({
                "user_id": uid,
                "job_posting_id": jid,
                "resume_url": (data.get("resume_url") or "").strip() or None,
                "cover_letter": (data.get("cover_letter") or "").strip() or None,
                "status": "pending",
            })
            return {
                "success": True,
                "application": app_rec.to_dict(),
                "error": None,
                "status_code": 201,
            }
        except Exception as e:
            return {
                "success": False,
                "application": None,
                "error": f"Database error: {str(e)}",
                "status_code": 500,
            }

    # ------------------------------------------------------------------
    # UPDATE STATUS / FULL UPDATE
    # ------------------------------------------------------------------

    @staticmethod
    def update_status(application_id: int, new_status: str, current_user: User | None) -> dict:
        """
        Update only the review status of an application.
        Restricted strictly to admin or the owner of the target job posting.
        """
        app_rec = Application.get_by_id(application_id)
        if app_rec is None:
            return {"success": False, "error": f"Application {application_id} not found.", "status_code": 404}

        if not ApplicationController.can_manage_application(app_rec, current_user):
            return {
                "success": False,
                "error": "Only an administrator or the owner of this job posting can update the application status.",
                "status_code": 403,
            }

        normalized = (new_status or "").strip().lower()
        if normalized not in VALID_STATUSES:
            return {
                "success": False,
                "error": f"Invalid status '{new_status}'. Allowed values: {', '.join(VALID_STATUSES)}.",
                "status_code": 400,
            }

        try:
            updated = Application.partial_update(application_id, {"status": normalized})
            return {
                "success": True,
                "application": updated.to_dict(),
                "message": f"Application #{application_id} status updated to '{normalized.capitalize()}'.",
                "status_code": 200,
            }
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}", "status_code": 500}

    @staticmethod
    def update(application_id: int, data: dict, current_user: User | None = None) -> dict:
        app_rec = Application.get_by_id(application_id)
        if app_rec is None:
            return {"success": False, "application": None, "error": f"Application {application_id} not found", "status_code": 404}

        if current_user is not None and not ApplicationController.can_manage_application(app_rec, current_user):
            return {
                "success": False,
                "application": None,
                "error": "Only an administrator or the owner of this job posting can edit this application.",
                "status_code": 403,
            }

        status = (data.get("status") or app_rec.status or "pending").strip().lower()
        if status not in VALID_STATUSES:
            return {
                "success": False,
                "application": None,
                "error": f"Invalid status '{status}'. Allowed values: {', '.join(VALID_STATUSES)}.",
                "status_code": 400,
            }

        try:
            updated = Application.partial_update(application_id, {
                "resume_url": (data.get("resume_url") or "").strip() or None,
                "cover_letter": (data.get("cover_letter") or "").strip() or None,
                "status": status,
            })
            return {"success": True, "application": updated.to_dict(), "error": None, "status_code": 200}
        except Exception as e:
            return {"success": False, "application": None, "error": f"Database error: {str(e)}", "status_code": 500}

    @staticmethod
    def delete(application_id: int, current_user: User | None = None) -> dict:
        app_rec = Application.get_by_id(application_id)
        if app_rec is None:
            return {"success": False, "message": f"Application {application_id} not found", "status_code": 404}

        if current_user is not None and not ApplicationController.can_manage_application(app_rec, current_user):
            return {
                "success": False,
                "message": "Only an administrator or the owner of this job posting can delete this application.",
                "status_code": 403,
            }

        try:
            Application.delete(application_id)
            return {"success": True, "message": f"Application #{application_id} deleted successfully.", "status_code": 200}
        except Exception as e:
            return {"success": False, "message": f"Database error: {str(e)}", "status_code": 500}
