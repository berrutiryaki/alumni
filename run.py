import os
from flask import Flask, jsonify
from flasgger import Swagger
from dotenv import load_dotenv

from app.database import db, migrate
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
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Alumni Platform</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; background-color: #f8f9fa; color: #333; }
        .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); max-width: 600px; }
        h1 { margin-top: 0; color: #212529; }
        ul { line-height: 2; font-size: 16px; }
        a { color: #0d6efd; text-decoration: none; font-weight: 500; }
        a:hover { text-decoration: underline; }
        .badge { background-color: #e8f5e9; color: #2e7d32; border: 1px solid #c8e6c9; padding: 4px 10px; border-radius: 12px; font-size: 13px; font-weight: 500; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Alumni Platform</h1>
        <p>Alumni Tracking & Networking Portal <span class="badge">Database Connected</span></p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 15px 0;">
        <h3>Web CRUD Interfaces</h3>
        <ul>
            <li><a href="/users">Users & Alumni Management (HTML)</a></li>
            <li><a href="/announcements">Announcements & Events Management (HTML)</a></li>
            <li><a href="/job-postings">Job Postings & Opportunities (HTML)</a></li>
            <li><a href="/applications">Job Applications Management (HTML)</a></li>
        </ul>
        <h3>REST API & Documentation</h3>
        <ul>
            <li><a href="/api/users">API Users (JSON)</a></li>
            <li><a href="/api/announcements">API Announcements (JSON)</a></li>
            <li><a href="/api/job-postings">API Job Postings (JSON)</a></li>
            <li><a href="/api/applications">API Applications (JSON)</a></li>
            <li><a href="/api/health">API Health Check (JSON)</a></li>
            <li><a href="/api/swagger">Interactive Swagger / OpenAPI Docs</a></li>
        </ul>
    </div>
</body>
</html>
""", 200, {"Content-Type": "text/html"}


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
