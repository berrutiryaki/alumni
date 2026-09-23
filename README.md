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

> **Current Status:** Early-stage. Core API skeleton is live with health-check endpoints. Database models and authentication are in active development.

---

## Modules & Features

### Currently Live

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root health-check |
| `/alumni` | GET | Alumni resource health-check |

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

## Project Structure

```
alumni/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   └── alumni.py
│   └── models/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/): `git commit -m 'feat: add mentorship endpoint'`
4. Open a Pull Request

---

## License

[MIT](LICENSE)