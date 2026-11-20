import os
from flask import Flask, jsonify, render_template
from flasgger import Swagger
from sqlalchemy import func
from dotenv import load_dotenv

from app.database import db, migrate
from app.middleware.logger import init_logger
from app.middleware.not_found_guardian import init_not_found_guardian
from app.middleware.server_error_guardian import init_server_error_guardian
from app.models.user import User
from app.models.announcement import Announcement
from app.models.job_posting import JobPosting
from app.models.application import Application
from app.routes.users import users_bp
from app.routes.api_users import api_users_bp
from app.routes.announcements import announcements_bp
from app.routes.api_announcements import api_announcements_bp
from app.routes.job_postings import job_postings_bp
from app.routes.api_job_postings import api_job_postings_bp
from app.routes.applications import applications_bp
from app.routes.api_applications import api_applications_bp

load_dotenv()

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates'))

# ------------------------------------------------------------------
# Database Configuration & Migration
# ------------------------------------------------------------------

database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

if not database_url:
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    database_url = f"sqlite:///{os.path.join(data_dir, 'alumni.db')}"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)

# Request logger middleware (time, method, route, status, duration)
init_logger(app)

# 404 guardian middleware (returns 404 errors with a reason)
init_not_found_guardian(app)

# 5xx guardian middleware (returns server errors with a reason)
init_server_error_guardian(app)

# ------------------------------------------------------------------
# Swagger / OpenAPI
# ------------------------------------------------------------------

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/api/swagger.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/swagger",
}

swagger_template = {
    "info": {
        "title": "Alumni API",
        "description": "Alumni Tracking & Networking Platform REST API",
        "version": "1.3.0",
    },
    "tags": [
        {"name": "Health", "description": "API status"},
        {"name": "Users", "description": "User CRUD via ApiUserController"},
        {"name": "Announcements", "description": "Announcement CRUD via ApiAnnouncementController"},
        {"name": "Job Postings", "description": "Job Posting CRUD via ApiJobPostingController"},
        {"name": "Applications", "description": "Job Application CRUD via ApiApplicationController"},
        {"name": "Users (Nested)", "description": "Nested user resources (announcements, applications)"},
        {"name": "Job Postings (Nested)", "description": "Nested job posting resources (applications)"},
    ],
}

Swagger(app, config=swagger_config, template=swagger_template)

# ------------------------------------------------------------------
# Blueprints
# ------------------------------------------------------------------

app.register_blueprint(users_bp)               # /users            — HTML
app.register_blueprint(api_users_bp)           # /api/users        — JSON
app.register_blueprint(announcements_bp)       # /announcements    — HTML
app.register_blueprint(api_announcements_bp)   # /api/announcements — JSON
app.register_blueprint(job_postings_bp)        # /job-postings     — HTML
app.register_blueprint(api_job_postings_bp)    # /api/job-postings — JSON
app.register_blueprint(applications_bp)        # /applications     — HTML
app.register_blueprint(api_applications_bp)    # /api/applications — JSON

# ------------------------------------------------------------------
# General routes
# ------------------------------------------------------------------


@app.route("/")
def index():
    stats = {
        "users_count": User.query.count(),
        "alumni_count": User.query.filter_by(status="alumni").count(),
        "student_count": User.query.filter_by(status="student").count(),
        "jobs_count": JobPosting.query.count(),
        "active_jobs_count": JobPosting.query.filter_by(is_active=True).count(),
        "applications_count": Application.query.count(),
        "pending_apps_count": Application.query.filter_by(status="pending").count(),
        "accepted_apps_count": Application.query.filter_by(status="accepted").count(),
        "announcements_count": Announcement.query.count(),
        "active_announcements_count": Announcement.query.filter_by(is_active=True).count(),
    }
    recent_jobs = (
        JobPosting.query.filter_by(is_active=True)
        .order_by(JobPosting.id.desc())
        .limit(4)
        .all()
    )
    recent_announcements = (
        Announcement.query.filter_by(is_active=True)
        .order_by(Announcement.id.desc())
        .limit(4)
        .all()
    )
    latest_app = Application.query.order_by(Application.id.desc()).first()
    dept_rows = (
        db.session.query(User.department, func.count(User.id).label("n"))
        .filter(User.department.isnot(None), User.department != "")
        .group_by(User.department)
        .order_by(func.count(User.id).desc())
        .limit(6)
        .all()
    )
    return render_template(
        "index.html",
        stats=stats,
        recent_jobs=recent_jobs,
        recent_announcements=recent_announcements,
        latest_application=latest_app.to_dict() if latest_app else None,
        departments=[row[0] for row in dept_rows],
    )


@app.route("/about")
def about():
    return """
<h1>About</h1>
<p>Alumni is a tracking and networking platform connecting graduates, students, and institutions.</p>
""", 200, {"Content-Type": "text/html"}


@app.route("/hello")
def hello():
    return "Hello, World!", 200, {"Content-Type": "text/plain"}


@app.route("/hello/<name>")
def hello_name(name):
    return f"Hello, {name.capitalize()}!", 200, {"Content-Type": "text/plain"}


@app.route("/sum/<int:number1>/<int:number2>")
def sum_numbers(number1, number2):
    return str(number1 + number2), 200, {"Content-Type": "text/plain"}


# ------------------------------------------------------------------
# Health check
# ------------------------------------------------------------------


@app.route("/api/health")
def health():
    """
    Health check endpoint.
    ---
    tags:
      - Health
    responses:
      200:
        description: API is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            message:
              type: string
              example: healthy
    """
    return jsonify({"status": "ok", "message": "healthy"}), 200


# Demo route to trigger a 5xx on purpose (only available in debug mode).
@app.route("/debug/500")
@app.route("/api/debug/500")
def debug_trigger_500():
    if not app.debug:
        from flask import abort
        abort(404, "Debug routes are disabled outside debug mode")
    raise RuntimeError("Intentional test error triggered from /debug/500")


# ------------------------------------------------------------------
# CLI Commands
# ------------------------------------------------------------------


@app.cli.command("seed")
def seed_command():
    """Seed the database with sample user and announcement records."""
    from app.seeds.database_seeder import DatabaseSeeder
    DatabaseSeeder.run()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
