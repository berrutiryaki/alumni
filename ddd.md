# Data Dictionary — Alumni Platform

This document describes the data models, field definitions, form mappings, and CRUD endpoint reference for the Alumni Platform API.

> See also: [README.md](README.md) — project overview, architecture, and getting started guide.

---

## User

**Model file:** [`app/models/user.py`](app/models/user.py)  
**Storage:** In-memory (no database — migration planned)  
**Controllers:** `UserController` (HTML) · `ApiUserController` (JSON API)

### Field Definitions

| Field | Python Type | Form Field (`name=`) | Required | Default | Notes |
|---|---|---|---|---|---|
| `id` | `int` | — | — | Auto-increment | Assigned by the model on create; not sent in form |
| `name` | `str` | `name` | Yes | — | Full name of the user |
| `email` | `str` | `email` | Yes | — | Must be unique per user |
| `status` | `str` | `status` | Yes | `"student"` | Accepted values: `alumni`, `student` |
| `department` | `str` | `department` | No | `None` | Academic department (e.g. Computer Engineering) |
| `graduation_year` | `int` | `graduation_year` | No | `None` | Only stored when `status = alumni`; ignored for students |

### Business Rules

- `graduation_year` is automatically set to `None` if `status` is `"student"` — even if a value is submitted.
- `name` and `email` are validated as required on both `POST` (create) and `PUT` (full update).
- `id` is never accepted from the client; it is always assigned server-side.

---

### CRUD Operations

#### Web Interface (HTML)

| Operation | Method | URL | Controller Method | View Template |
|---|---|---|---|---|
| List all users | `GET` | `/users/` | `UserController.index()` | `user/index.html` |
| Show create form | `GET` | `/users/new` | — | `user/create.html` |
| Create user | `POST` | `/users/` | `UserController.create(data)` | Redirects to list on success |
| Show edit form | `GET` | `/users/<id>/edit` | `UserController.show(id)` | `user/edit.html` |
| Update user | `POST` | `/users/<id>/edit` | `UserController.update(id, data)` | Redirects to list on success |
| Delete user | `POST` | `/users/<id>/delete` | `UserController.delete(id)` | Redirects to list on success |

#### REST API (JSON)

| Operation | Method | URL | Controller Method | Success Code |
|---|---|---|---|---|
| List all users | `GET` | `/api/users/` | `ApiUserController.index()` | `200 OK` |
| Get user by ID | `GET` | `/api/users/<id>` | `ApiUserController.show(id)` | `200 OK` |
| Create user | `POST` | `/api/users/` | `ApiUserController.create()` | `201 Created` |
| Full update | `PUT` | `/api/users/<id>` | `ApiUserController.update(id)` | `200 OK` |
| Partial update | `PATCH` | `/api/users/<id>` | `ApiUserController.partial_update(id)` | `200 OK` |
| Delete user | `DELETE` | `/api/users/<id>` | `ApiUserController.delete(id)` | `200 OK` |

#### API Error Responses

| Status Code | Condition |
|---|---|
| `400 Bad Request` | Missing required field (`name` or `email`) |
| `404 Not Found` | No user found with the given `id` |

---

### Postman — Form-Data Examples

**POST /api/users/** — Create a student

| Key | Value |
|---|---|
| `name` | Berru |
| `email` | berru@example.com |
| `status` | student |
| `department` | Computer Engineering |

**POST /api/users/** — Create an alumni

| Key | Value |
|---|---|
| `name` | Ali Yılmaz |
| `email` | ali@example.com |
| `status` | alumni |
| `department` | Business Administration |
| `graduation_year` | 2022 |

**PATCH /api/users/1** — Partial update (only email)

| Key | Value |
|---|---|
| `email` | newemail@example.com |

**PUT /api/users/1** — Full replace (all fields required)

| Key | Value |
|---|---|
| `name` | Berru Updated |
| `email` | berru2@example.com |
| `status` | alumni |
| `department` | Computer Engineering |
| `graduation_year` | 2025 |

---

## Announcement

**Model file:** [`app/models/announcement.py`](app/models/announcement.py)  
**Storage:** In-memory (no database — migration planned)  
**Controllers:** `AnnouncementController` (HTML) · `ApiAnnouncementController` (JSON API)

### Field Definitions

| Field | Python Type | Form Field (`name=`) | Required | Default | Notes |
|---|---|---|---|---|---|
| `id` | `int` | — | — | Auto-increment | Assigned by the model on create |
| `title` | `str` | `title` | Yes | — | Short headline for the announcement |
| `content` | `str` | `content` | Yes | — | Full body text of the announcement |
| `author` | `str` | `author` | No | `None` | Display name of the person posting |
| `is_active` | `bool` | `is_active` | No | `True` | Accepted form values: `true` / `false` |
| `created_at` | `str` | — | — | `datetime.now()` | Set automatically on creation; not editable |

### Business Rules

- `title` and `content` are required on both create and full update.
- `is_active` accepts the string values `"true"` / `"false"` from form-data; these are converted to `bool` internally.
- `created_at` is set once at creation time and never modified.

---

### CRUD Operations

#### Web Interface (HTML)

| Operation | Method | URL | Controller Method | View Template |
|---|---|---|---|---|
| List all | `GET` | `/announcements/` | `AnnouncementController.index()` | `announcement/index.html` |
| Show create form | `GET` | `/announcements/new` | — | `announcement/create.html` |
| Create | `POST` | `/announcements/` | `AnnouncementController.create(data)` | Redirects to list on success |
| Show edit form | `GET` | `/announcements/<id>/edit` | `AnnouncementController.show(id)` | `announcement/edit.html` |
| Update | `POST` | `/announcements/<id>/edit` | `AnnouncementController.update(id, data)` | Redirects to list on success |
| Delete | `POST` | `/announcements/<id>/delete` | `AnnouncementController.delete(id)` | Redirects to list on success |

#### REST API (JSON)

| Operation | Method | URL | Controller Method | Success Code |
|---|---|---|---|---|
| List all | `GET` | `/api/announcements/` | `ApiAnnouncementController.index()` | `200 OK` |
| Get by ID | `GET` | `/api/announcements/<id>` | `ApiAnnouncementController.show(id)` | `200 OK` |
| Create | `POST` | `/api/announcements/` | `ApiAnnouncementController.create()` | `201 Created` |
| Full update | `PUT` | `/api/announcements/<id>` | `ApiAnnouncementController.update(id)` | `200 OK` |
| Partial update | `PATCH` | `/api/announcements/<id>` | `ApiAnnouncementController.partial_update(id)` | `200 OK` |
| Delete | `DELETE` | `/api/announcements/<id>` | `ApiAnnouncementController.delete(id)` | `200 OK` |

#### API Error Responses

| Status Code | Condition |
|---|---|
| `400 Bad Request` | Missing `title` or `content` |
| `404 Not Found` | No announcement found with the given `id` |

---

### Postman — Form-Data Examples

**POST /api/announcements/** — Create an active announcement

| Key | Value |
|---|---|
| `title` | Spring Career Fair 2025 |
| `content` | Join us on April 10th for the annual career fair at the main campus. |
| `author` | Admin |
| `is_active` | true |

**PATCH /api/announcements/1** — Deactivate an announcement

| Key | Value |
|---|---|
| `is_active` | false |

---

## Swagger / OpenAPI

Interactive API documentation is available at:

```
http://localhost:5000/api/swagger
```

All `/api/users` and `/api/announcements` endpoints are documented there with request parameters and response schemas.
