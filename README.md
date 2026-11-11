# Alumni

Alumni Tracking & Networking Platform — universities, graduates, and students in one ecosystem.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## Overview

Universities lose contact with graduates the moment they leave campus. Alumni solves this by providing a centralized, API-first platform for managing graduate profiles, career tracking, mentorship, and community engagement — keeping institutions and alumni connected long after graduation.

> **Data Dictionary & Documentation Rule:** For field definitions, form mappings, and CRUD endpoint reference, see [ddd.md](ddd.md). **Rule:** Whenever any data model, field, type, form mapping, or CRUD endpoint is added, modified, or deleted, [ddd.md](ddd.md) **MUST** be updated immediately to maintain documentation integrity.

> **Current Status:** Core API skeleton, database models (SQLAlchemy), migrations (Flask-Migrate), seeders, and full CRUD interfaces are live with Swagger documentation.

---

## Modules & Features

### Currently Live

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `GET` | Root portal & quick navigation |
| `/users` | `GET, POST` | Users & Alumni web CRUD interface (HTML) |
| `/announcements` | `GET, POST` | Announcements web CRUD interface (HTML) |
| `/job-postings` | `GET, POST` | Job Postings web CRUD interface (HTML) |
| `/applications` | `GET, POST` | Job Applications (Action Table) web CRUD interface (HTML) |
| `/404` | `GET` | Generic 404 Not Found page (invalid web requests redirect here) |
| `/api/users` | `GET, POST, PUT, PATCH, DELETE` | Users REST API + nested `/announcements` & `/applications` |
| `/api/announcements` | `GET, POST, PUT, PATCH, DELETE` | Announcements REST API |
| `/api/job-postings` | `GET, POST, PUT, PATCH, DELETE` | Job Postings REST API + nested `/applications` |
| `/api/applications` | `GET, POST, PUT, PATCH, DELETE` | Applications REST API |
| `/api/health` | `GET` | API health check |
| `/api/swagger` | `GET` | Interactive Swagger / OpenAPI documentation |

### Roadmap

**Profile Management** — Full CRUD for alumni profiles: academic history, graduation year, department, employer, location, and privacy controls.

**Alumni Search & Filtering** — Query the alumni directory by graduation year, department, industry, company, location, or skill. Supports both user-facing discovery and institutional reporting.

**Career Board** — Job and internship listings posted by alumni-owned companies and institutional partners.

**Mentorship Network** — Structured mentor-mentee matching with scheduling, goal tracking, and session logging.

**Event Management** — End-to-end event lifecycle: creation, RSVP, attendance tracking, and post-event analytics.

**Authentication & Authorization** — JWT-based auth with role-based access control (Alumni, Student, Faculty, Admin).

---

## Technology Stack

| Technology | Reason | Trade-off |
|------------|--------|-----------|
| Python 3.12 + Flask 3.x | Minimal boilerplate, fast iteration, large ecosystem | Slower than compiled languages under high concurrency |
| PostgreSQL 16 | Relational integrity, JSONB, built-in full-text search | Higher operational overhead than SQLite; requires proper database administration in production |
| Docker & Docker Compose | Reproducible environment, single-command setup | Requires Docker Desktop; adds a layer between developer and underlying services |
| Antigravity | Integrated agentic AI assistant, free in development | AI output requires human review; suggestions may need iteration |

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

No local Python or PostgreSQL installation is required.

### Run

```bash
git clone https://github.com/berrutiryaki/alumni.git
cd alumni
docker compose up
```

This starts the Flask API and PostgreSQL database together. The API is available at `http://localhost:5000`.

### Verify

```bash
curl http://localhost:5000/
curl http://localhost:5000/alumni
```

### Stop

```bash
# Stop containers, preserve data
docker compose down

# Stop and wipe all data
docker compose down -v
```

### Detached mode

```bash
docker compose up -d
docker compose logs -f
```

---

## Architecture

The project follows the **MVC (Model-View-Controller)** pattern adapted for a REST API context. In an API-first application there are no server-rendered views; the "View" layer is replaced by **Serializers / Response Schemas** that shape the JSON output returned to clients.

```
MVC Layer        REST API Equivalent       Responsibility
-----------      ---------------------     ----------------------------------------
Model            models/                   Data structure, database schema, ORM logic
View             serializers/ + JSON       Shape and format the HTTP response body
Controller       routes/ (Blueprints)      Handle requests, call services, return responses
```

### Directory Structure

```
alumni/
│
├── app/                          # Application package
│   ├── database.py               # SQLAlchemy and Migrate instances
│   │
│   ├── middleware/               # Request logging & error guardian middlewares
│   │   ├── __init__.py
│   │   ├── logger.py             # Terminal request logger (time, method, route, status, duration)
│   │   ├── not_found_guardian.py # 404 Guardian (JSON reason for API, redirect to /404 for web)
│   │   ├── server_error_guardian.py # 5xx Guardian (catches 5xx & unhandled exceptions with reason)
│   │   └── error_log.py          # File logger appending 404 & 5xx errors to logs/error.logs
│   │
│   ├── models/                   # MODEL layer (SQLAlchemy db.Model)
│   │   ├── __init__.py
│   │   ├── user.py               # User model & table
│   │   ├── announcement.py       # Announcement model & table (FK -> users)
│   │   ├── job_posting.py        # JobPosting model & table (independent)
│   │   └── application.py        # Application Action Table (FK -> users, job_postings)
│   │
│   ├── controllers/              # Controller layer (HTML & JSON API)
│   │   ├── user_controller.py
│   │   ├── api_user_controller.py
│   │   ├── announcement_controller.py
│   │   ├── api_announcement_controller.py
│   │   ├── job_posting_controller.py
│   │   ├── api_job_posting_controller.py
│   │   ├── application_controller.py
│   │   └── api_application_controller.py
│   │
│   ├── routes/                   # Route Blueprints
│   │   ├── users.py              # HTML routes (/users)
│   │   ├── api_users.py          # REST API routes (/api/users + nested routes)
│   │   ├── announcements.py      # HTML routes (/announcements)
│   │   ├── api_announcements.py  # REST API routes (/api/announcements)
│   │   ├── job_postings.py       # HTML routes (/job-postings)
│   │   ├── api_job_postings.py   # REST API routes (/api/job-postings + nested routes)
│   │   ├── applications.py       # HTML routes (/applications)
│   │   └── api_applications.py   # REST API routes (/api/applications)
│   │
│   ├── templates/                # Jinja2 HTML views
│   │   ├── 404.html              # Generic 404 Not Found page
│   │   ├── user/
│   │   ├── announcement/
│   │   ├── job_posting/
│   │   └── application/
│   │
│   ├── factories/                # Factory pattern data generators
│   │   ├── user_factory.py       # UserFactory (build, create, create_batch)
│   │   ├── announcement_factory.py # AnnouncementFactory
│   │   ├── job_posting_factory.py # JobPostingFactory
│   │   └── application_factory.py # ApplicationFactory
│   │
│   └── seeds/                    # Database Seeders
│       ├── database_seeder.py    # Main seeder orchestrator
│       ├── user_seeder.py        # Seeds student & alumni records
│       ├── announcement_seeder.py # Seeds announcement records
│       ├── job_posting_seeder.py # Seeds job posting records
│       └── application_seeder.py # Seeds multi-user job applications
│
├── logs/                         # Error log directory (error.logs)
├── migrations/                   # Alembic database migration versions
├── run.py                        # Entry point — app config, middlewares & server startup
├── seed.py                       # CLI script to seed the database
├── ddd.md                        # Data Dictionary & Relationship Matrix
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container image definition
├── docker-compose.yml            # Multi-container orchestration (Web + PostgreSQL 16)
├── example.env                   # Example environment variable template
└── README.md
```

### Middleware & Error Handling

1. **Terminal Request Logger (`app/middleware/logger.py`)**
   Logs every incoming HTTP request to the terminal in a tabular format:
   ```text
   time        method   route                           status  duration
   10:20:30    POST     /api/users                      201     18ms
   ```
2. **404 Guardian & Generic `/404` Redirect (`app/middleware/not_found_guardian.py`)**
   - Catches all `404 Not Found` errors and records them in `logs/error.logs`.
   - For `/api/*` routes: returns a structured `404` JSON payload containing `reason`, `path`, and close-match `suggestions`.
   - For web routes: redirects (`302`) invalid URLs or non-existent resource requests to the generic `/404` page (`app/templates/404.html`), displaying the reason and route suggestions.
3. **5xx Guardian (`app/middleware/server_error_guardian.py`)**
   - Catches `500–504` HTTP errors and any unhandled runtime exceptions.
   - Returns structured JSON (for `/api/*`) or an HTML error card (for web routes) with `reason` and `error_type`, while printing the full traceback to the terminal and appending it to `logs/error.logs`.
4. **Error File Logger (`app/middleware/error_log.py`)**
   - Persists all `404` and `5xx` errors to `logs/error.logs` with automatic log rotation (`RotatingFileHandler`).

### Database Migrations & Seeding

**Running Migrations:**
```bash
# Generate a new migration after model changes
python -m flask --app run db migrate -m "Description of changes"

# Apply pending migrations to the database
python -m flask --app run db upgrade
```

**Seeding the Database with Mock Data:**
```bash
# Populate database using factories (Users, Announcements, Job Postings, Applications)
python seed.py

# Or clear existing data first, then seed fresh records:
python seed.py --clean

# Alternatively via Flask CLI:
python -m flask --app run seed
```

**Using Factories Programmatically:**
```python
from app.factories import (
    UserFactory,
    AnnouncementFactory,
    JobPostingFactory,
    ApplicationFactory,
)

# Create single records
student = UserFactory.create_student()
alumni = UserFactory.create_alumni(graduation_year=2020)

# Create batch
users = UserFactory.create_batch(10)
announcements = AnnouncementFactory.create_batch(5)
jobs = JobPostingFactory.create_batch(5)
applications = ApplicationFactory.create_batch(8)
```

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Update documentation: **`ddd.md` must be kept up-to-date with any changes to models, fields, or endpoints.**
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/): `git commit -m 'feat: add mentorship endpoint'`
5. Open a Pull Request

---

## License

[MIT](LICENSE)