# Data Dictionary — Alumni Platform

This document describes the data models, field definitions, form mappings, and CRUD endpoint reference for the Alumni Platform API.

> See also: [README.md](README.md) — project overview, architecture, and getting started guide.

---

## Database Schema & Entity Relationships

This section provides a bird's-eye view of all tables in the Alumni Platform, their primary keys, foreign keys, and cardinalities.

> **Architecture Note:** `users` ve `job_postings` tabloları arasında **doğrudan yabancı anahtar (FK) bağlantısı yoktur**. `applications` tablosu, aday (`users`) ile iş ilanı (`job_postings`) arasındaki **Eylem Tablosu (Action / Junction Table)** olarak görev yapar ve Çoktan-Çoğa (Many-to-Many) ilişkiyi kurar.

### Entity-Relationship Diagram

```
┌──────────────────────────────────────┐             ┌──────────────────────────────────┐
│                users                 │             │           job_postings           │
├──────────────────────────────────────┤             ├──────────────────────────────────┤
│ PK  id               Integer         │             │ PK  id               Integer     │
│     name             String(120)     │             │     title            String(120) │
│ UQ  email            String(120)     │             │     company          String(120) │
│     password_hash    String(255)     │             │     city             String(120) │
│     role             String(30)      │             │     description      Text        │
│     status           String(20)      │             │     employment_type  String(50)  │
│     department       String(120)     │             │     salary_range     String(100) │
│     graduation_year  Integer         │             │     posted_by        String(100) │
└──────────────────────────────────────┘             │     is_active        Boolean     │
         │ N (user_id)           │ N (user_id)       │     created_at       String(30)  │
         ▼                       ▼                   │     expires_at       String(50)  │
┌──────────────────┐    ┌──────────────────────────────────┐ └──────────────────────────────────┘
│  announcements   │    │          applications            │                   │ 1
├──────────────────┤    │          (Action Table)          │                   │
│ PK id  Integer   │    ├──────────────────────────────────┤                   │ N (job_posting_id)
│ FK user_id (opt) │    │ PK id              Integer       │◀──────────────────┘
│    title         │    │ FK user_id (req)   Integer (FK)  │
│    content       │    │ FK job_posting_id  Integer (FK)  │
│    author        │    │    resume_url      String(255)   │
│    is_active     │    │    cover_letter    Text          │
│    created_at    │    │    status          String(50)    │
└──────────────────┘    │    applied_at      String(30)    │
                        └──────────────────────────────────┘
```

```mermaid
erDiagram
    users ||--o{ announcements : "authors (1:N)"
    users ||--o{ applications : "submits (1:N)"
    job_postings ||--o{ applications : "receives (1:N)"

    users {
        int id PK
        string name
        string email UK
        string password_hash
        string role
        string status
        string department
        int graduation_year
    }

    announcements {
        int id PK
        int user_id FK
        string title
        text content
        string author
        boolean is_active
        string created_at
    }

    job_postings {
        int id PK
        string title
        string company
        string city
        text description
        string employment_type
        string salary_range
        string posted_by
        boolean is_active
        string created_at
        string expires_at
    }

    applications {
        int id PK
        int user_id FK
        int job_posting_id FK
        string resume_url
        text cover_letter
        string status
        string applied_at
    }
```

### Master Relationship Matrix

| # | Kaynak Tablo (Source) | Kaynak Kolon (FK) | Hedef Tablo (Target) | Hedef Kolon (PK) | İlişki Türü (Cardinality) | İş Mantığı / Açıklama |
|---|---|---|---|---|---|---|
| 1 | `announcements` | `user_id` | `users` | `id` | Many-to-One (`N:1`) | Bir duyuruyu bir kullanıcı (yazar) yayınlar. Opsiyoneldir (`nullable=True`). |
| 2 | `applications` | `user_id` | `users` | `id` | Many-to-One (`N:1`) | Her iş başvurusunu kayıtlı bir kullanıcı (öğrenci/mezun) yapar. Zorunludur (`nullable=False`). |
| 3 | `applications` | `job_posting_id` | `job_postings` | `id` | Many-to-One (`N:1`) | Her iş başvurusu belirli bir iş ilanına yöneliktir. Zorunludur (`nullable=False`). |
| 4 | `users` | `id` | `announcements` | `user_id` | One-to-Many (`1:N`) | Bir kullanıcının yayınladığı birden fazla duyuru bulunabilir (`user.announcements`). |
| 5 | `users` | `id` | `applications` | `user_id` | One-to-Many (`1:N`) | Bir kullanıcının yaptığı birden fazla iş başvurusu bulunabilir (`user.applications`). |
| 6 | `job_postings` | `id` | `applications` | `job_posting_id` | One-to-Many (`1:N`) | Bir iş ilanına birden fazla başvuru gelebilir (`job_posting.applications`). |
| **Action** | `applications` | `(user_id, job_posting_id)` | `users` & `job_postings` | `id` | **Action / Junction Table** | `users` ile `job_postings` arasında doğrudan FK yoktur. `applications` tablosu aralarındaki bağlantıyı sağlayan eylem tablosudur. |

### Tables Summary

| Tablo Adı | Model Sınıfı | Dosya | Primary Key | Foreign Keys | Toplam Alan | Açıklama |
|---|---|---|---|---|---|---|
| `users` | `User` | `app/models/user.py` | `id` | — | 6 | Kullanıcı profilleri ve sistem rolleri (`student`, `alumni`, `academician`, `admin`) |
| `announcements` | `Announcement` | `app/models/announcement.py` | `id` | `user_id → users.id` | 7 | Etkinlik ve genel duyurular |
| `job_postings` | `JobPosting` | `app/models/job_posting.py` | `id` | — | 10 | İş ve staj fırsat ilanları (bağımsız) |
| `applications` | `Application` | `app/models/application.py` | `id` | `user_id → users.id`<br>`job_posting_id → job_postings.id` | 7 | Eylem tablosu: Kullanıcıların iş ilanlarına başvuruları |

---

## User & System Roles (RBAC)

**Model file:** [`app/models/user.py`](app/models/user.py)  
**Storage:** Database via SQLAlchemy & Flask-Migrate (PostgreSQL in Docker / SQLite fallback)  
**Controllers:** `UserController` (HTML) · `ApiUserController` (JSON API)

### Field Definitions

| Field | Python Type | Form Field (`name=`) | Required | Default | Notes |
|---|---|---|---|---|---|
| `id` | `int` | — | — | Auto-increment | Assigned by the model on create; not sent in form |
| `name` | `str` | `name` | Yes | — | Full name of the user |
| `email` | `str` | `email` | Yes | — | Must be unique per user |
| `password_hash` | `str` | `password` / `confirm_password` | Yes *(on `/register`)* | `None` | Hashed via `werkzeug.security.generate_password_hash`; plain text is never stored |
| `role` | `str` | `role` | Yes | `"student"` | System role: `student`, `alumni`, `academician`, `admin` (visitors act as `guest`) |
| `status` | `str` | `status` | Yes | `"student"` | Legacy alias synchronized with `role` (`student`, `alumni`, `academician`, `admin`) |
| `department` | `str` | `department` | No | `None` | Academic department (e.g. Computer Engineering) |
| `graduation_year` | `int` | `graduation_year` | No | `None` | Stored when `role = alumni`; automatically `None` for `student`, `academician`, and `admin` |

### System Roles & Actor Definitions

Platformda **5 temel kullanıcı rolü (aktör)** tanımlanmıştır. Kayıtsız ziyaretçiler `guest`, kayıtlı kullanıcılar ise `users.status` alanındaki değere göre (`student`, `alumni`, `academician`, `admin`) yetkilendirilir:

| Rol | Kod Değeri (`status`) | Kimlik / Tanım | Temel Sorumluluk ve Yetkiler |
|---|---|---|---|
| **1. Guest (Ziyaretçi)** | `guest` *(oturumsuz)* | Sisteme giriş yapmamış veya henüz kayıt olmamış ziyaretçi | • Ana sayfayı (`/`), aktif duyuruları (`/announcements`) ve açık iş ilanlarını (`/job-postings`) salt-okunur (*read-only*) görüntüleyebilir.<br>• İş veya mentorluk başvurusu yapamaz, içerik yayınlayamaz. |
| **2. Student (Öğrenci)** | `student` | Üniversitede öğrenimine devam eden aktif öğrenci | • **İş & Staj Başvurusu:** Açık iş ve staj ilanlarına başvuru (`Application`) yapabilir, başvuru durumunu takip edebilir.<br>• **Mentorluk Başvurusu:** Mezunların ve akademisyenlerin açtığı mentorluk programlarına *mentee* (danışan) olarak başvurabilir.<br>• **Kısıtlama:** Mentorluk programı açamaz (*mentor* olamaz), iş ilanı yayınlayamaz. |
| **3. Alumni (Mezun)** | `alumni` | Üniversiteden mezun olmuş kullanıcı (`graduation_year` sahibi) | • **İş Başvurusu:** Tıpkı öğrenciler gibi açık iş ilanlarına başvuru (`Application`) yapabilir.<br>• **İş & Staj İlanı Açma:** Çalıştığı veya kurucusu olduğu şirket adına iş/staj ilanı (`JobPosting`) yayınlayabilir.<br>• **Mentorluk Açma:** Öğrencilere ve yeni mezunlara kariyer rehberliği için **mentorluk programı açabilir** (*mentor* olabilir) ve başvuruları kabul/reddedebilir.<br>• **Duyuru:** Mezun buluşması ve kariyer etkinlikleri için duyuru paylaşabilir. |
| **4. Academician (Akademisyen)** | `academician` | Üniversite öğretim üyesi, araştırma görevlisi veya bölüm koordinatörü | • **Akademik Duyuru & Etkinlik:** Seminer, burs, konferans ve bölüm duyuruları (`Announcement`) yayınlayabilir.<br>• **Araştırma & Asistanlık İlanı:** Araştırma projeleri ve laboratuvar çalışmaları için ilan (`JobPosting`) açabilir.<br>• **Akademik Mentorluk:** Öğrencilere akademik/tez/kariyer mentorluğu açabilir ve gelen öğrenci başvurularını değerlendirebilir.<br>• **Kısıtlama:** Ticari iş ilanlarına aday olarak başvurmaz. |
| **5. Admin (Yönetici)** | `admin` | Platform yöneticisi (Kariyer Merkezi / Mezunlar Ofisi / Sistem Admini) | • **Tam Sistem Yetkisi (Full CRUD):** Tüm kullanıcı profillerini, duyuruları, iş ilanlarını, iş başvurularını ve mentorluk kayıtlarını oluşturabilir, düzenleyebilir, onaylayabilir veya silebilir.<br>• **Rol & Moderasyon:** Kullanıcı rollerini (`student` → `alumni`, `academician`, `admin`) güncelleyebilir, başvuru durumlarını (`pending` → `reviewed` / `accepted` / `rejected`) yönetebilir. |

### Role Permission Matrix (Yetki Matrisi)

| İşlem / Modül Yetkisi | Guest (`guest`) | Student (`student`) | Alumni (`alumni`) | Academician (`academician`) | Admin (`admin`) |
|---|:---:|:---:|:---:|:---:|:---:|
| Ana sayfa, duyuru ve iş ilanlarını görüntüleme | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kendi profilini oluşturma ve düzenleme | ❌ *(Kayıt olur)* | ✅ | ✅ | ✅ | ✅ |
| **İş / Staj İlanına Başvuru Yapma (`Application`)** | ❌ | ✅ | ✅ | ❌ | ✅ |
| **İş / Staj / Araştırma İlanı Açma (`JobPosting`)** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Mentorluk Programı Açma (*Mentor* olma)** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Mentorluk Programına Başvurma (*Mentee* olma)** | ❌ | ✅ | ✅ *(Yeni mezun)* | ❌ | ✅ |
| **Duyuru ve Etkinlik Yayınlama (`Announcement`)** | ❌ | ❌ | ✅ | ✅ | ✅ |
| Başvuru durumlarını (`accepted` / `rejected`) güncelleme | ❌ | ❌ *(Sadece görüntüler)* | ✅ *(Kendi ilanında)* | ✅ *(Kendi ilanında)* | ✅ *(Tümünde)* |
| Tüm kayıtlar üzerinde tam CRUD ve moderasyon | ❌ | ❌ | ❌ | ❌ | ✅ |

```mermaid
flowchart TD
    Guest["Guest (Ziyaretçi)"] -->|Salt-Okunur Görüntüler| Public["Duyurular & İş İlanları"]
    Student["Student (Öğrenci)"] -->|İş/Staj Başvurusu Yapar| App["Application (İş Başvurusu)"]
    Student -->|Mentee Olarak Başvurur| Mentorship["Mentorship (Mentorluk)"]
    Alumni["Alumni (Mezun)"] -->|İş Başvurusu Yapar| App
    Alumni -->|İş/Staj İlanı Açar| Job["JobPosting (İş İlanı)"]
    Alumni -->|Mentorluk Programı Açar| Mentorship
    Alumni -->|Etkinlik/Duyuru Paylaşır| Ann["Announcement (Duyuru)"]
    Academician["Academician (Akademisyen)"] -->|Bölüm/Burs Duyurusu Açar| Ann
    Academician -->|Araştırma/Staj İlanı Açar| Job
    Academician -->|Akademik Mentorluk Açar| Mentorship
    Admin["Admin (Sistem Yöneticisi)"] -->|Tam CRUD & Moderasyon| All["Tüm Modüller (Users, Jobs, Apps, Announcements, Mentorship)"]
```

### Relationships

| Relationship | Type | Target Model | Foreign Key | Notes |
|---|---|---|---|---|
| `announcements` | One-to-Many | `Announcement` | `announcements.user_id → users.id` | A user (`alumni`, `academician`, `admin`) can author many announcements |
| `applications` | One-to-Many | `Application` | `applications.user_id → users.id` | A user (`student`, `alumni`) can submit many job applications (Action Table) |

### Business Rules

- Accepted registered user roles (`status`) are: `student`, `alumni`, `academician`, and `admin` (unauthenticated sessions are treated as `guest`).
- `graduation_year` is stored only when `status` is `"alumni"`; it is automatically set to `None` if `status` is `"student"`, `"academician"`, or `"admin"`.
- Both `student` and `alumni` users can submit job applications (`Application` action table).
- `alumni`, `academician`, and `admin` users can publish job/internship postings (`JobPosting`) and open mentorship programs; `student` users (and junior `alumni`) can apply to mentorship programs.
- `name` and `email` are validated as required on both `POST` (create) and `PUT` (full update).
- `id` is never accepted from the client; it is always assigned server-side.

---

### CRUD Operations

#### Web Interface (HTML)

| Operation | Method | URL | Controller Method | View Template |
|---|---|---|---|---|
| Show registration form | `GET` | `/register` | — | `register.html` |
| Register & auto-login | `POST` | `/register` | `UserController.register(data)` | Sets `session['user_id']`, redirects to `/` |
| Show login form | `GET` | `/login` | — | `login.html` |
| Authenticate user | `POST` | `/login` | `UserController.login(data)` | Sets `session['user_id']`, redirects to `/` |
| Log out user | `POST` | `/logout` | — | Clears `session`, redirects to `/` |
| List all users | `GET` | `/users/` | `UserController.index()` | `user/index.html` |
| View user profile | `GET` | `/users/<id>` | `UserController.show(id)` | `user/show.html` |
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

#### Nested Endpoints (under User)

| Operation | Method | URL | Description | Success Code |
|---|---|---|---|---|
| List user's announcements | `GET` | `/api/users/<user_id>/announcements` | Returns all announcements authored by this user | `200 OK` |
| Create user's announcement | `POST` | `/api/users/<user_id>/announcements` | Creates an announcement associated with this user | `201 Created` |
| List user's applications | `GET` | `/api/users/<user_id>/applications` | Returns all job applications submitted by this user | `200 OK` |
| Create user's application | `POST` | `/api/users/<user_id>/applications` | Submits a new job application as this user | `201 Created` |

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
**Storage:** Database via SQLAlchemy & Flask-Migrate (PostgreSQL in Docker / SQLite fallback)  
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
| `user_id` | `int` | `user_id` | No | `None` | FK → `users.id`; links announcement to the author user |

### Relationships

| Relationship | Type | Target Model | Foreign Key | Notes |
|---|---|---|---|---|
| `user` | Many-to-One | `User` | `announcements.user_id → users.id` | The user who created this announcement |

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

## JobPosting

**Model file:** [`app/models/job_posting.py`](app/models/job_posting.py)  
**Storage:** Database via SQLAlchemy & Flask-Migrate (PostgreSQL in Docker / SQLite fallback)  
**Controllers:** `JobPostingController` (HTML) · `ApiJobPostingController` (JSON API)

### Field Definitions

| Field | Python Type | DB Type | Form Field (`name=`) | Required | Default | Notes |
|---|---|---|---|---|---|---|
| `id` | `int` | `Integer` PK | — | — | Auto-increment | Assigned by the model on create; not sent in form |
| `title` | `str` | `String(120)` | `title` | Yes | — | Job position title (max 120 characters) |
| `company` | `str` | `String(120)` | `company` | Yes | — | Hiring company / organization name (max 120 characters) |
| `city` | `str` | `String(120)` | `city` | No | `None` | Work city / location (optional, max 120 characters; e.g. "Istanbul", "Remote") |
| `description` | `str` | `Text` | `description` | No | `None` | Full job description, responsibilities, requirements (optional) |
| `employment_type` | `str` | `String(50)` | `employment_type` | Yes | `"full-time"` | Required. Accepted: `full-time`, `part-time`, `internship`, `contract`, `remote` |
| `salary_range` | `str` | `String(100)` | `salary_range` | Yes | — | Required salary info (e.g. "15.000-25.000 TL") |
| `posted_by` | `str` | `String(100)` | `posted_by` | No | `None` | Name or email of the person who posted the job |
| `is_active` | `bool` | `Boolean` | `is_active` | No | `True` | Accepted form values: `true` / `false` |
| `created_at` | `str` | `DateTime` | — | — | `datetime.now()` | Set automatically on creation; not editable |
| `expires_at` | `str` | `String(50)` | `expires_at` | No | `None` | Expiration date (e.g. "2025-12-31"); informational only |

### Relationships

| Relationship | Type | Target Model | Foreign Key | Notes |
|---|---|---|---|---|
| `applications` | One-to-Many | `Application` | `applications.job_posting_id → job_postings.id` | Candidates who applied to this job posting (Action Table) |

### Business Rules

- `title` is required and has a maximum length of 120 characters (`String(120)`).
- `company` is required and has a maximum length of 120 characters (`String(120)`).
- `employment_type` and `salary_range` are required on both `POST` (create) and `PUT` (full update).
- `city` and `description` are optional (`nullable=True`).
- `is_active` accepts the string values `"true"` / `"false"` from form-data; these are converted to `bool` internally.
- `created_at` is set once at creation time and never modified.
- `expires_at` is informational; no automatic deactivation is performed when the date passes.
- `id` is never accepted from the client; it is always assigned server-side.

---

### CRUD Operations

#### Web Interface (HTML)

| Operation | Method | URL | Controller Method | View Template |
|---|---|---|---|---|
| List all | `GET` | `/job-postings/` | `JobPostingController.index()` | `job_posting/index.html` |
| Show create form | `GET` | `/job-postings/new` | — | `job_posting/create.html` |
| Create | `POST` | `/job-postings/` | `JobPostingController.create(data)` | Redirects to list on success |
| Show edit form | `GET` | `/job-postings/<id>/edit` | `JobPostingController.show(id)` | `job_posting/edit.html` |
| Update | `POST` | `/job-postings/<id>/edit` | `JobPostingController.update(id, data)` | Redirects to list on success |
| Delete | `POST` | `/job-postings/<id>/delete` | `JobPostingController.delete(id)` | Redirects to list on success |

#### REST API (JSON)

| Operation | Method | URL | Controller Method | Success Code |
|---|---|---|---|---|
| List all | `GET` | `/api/job-postings/` | `ApiJobPostingController.index()` | `200 OK` |
| Get by ID | `GET` | `/api/job-postings/<id>` | `ApiJobPostingController.show(id)` | `200 OK` |
| Create | `POST` | `/api/job-postings/` | `ApiJobPostingController.create()` | `201 Created` |
| Full update | `PUT` | `/api/job-postings/<id>` | `ApiJobPostingController.update(id)` | `200 OK` |
| Partial update | `PATCH` | `/api/job-postings/<id>` | `ApiJobPostingController.partial_update(id)` | `200 OK` |
| Delete | `DELETE` | `/api/job-postings/<id>` | `ApiJobPostingController.delete(id)` | `200 OK` |

#### Nested Endpoints (under JobPosting)

| Operation | Method | URL | Description | Success Code |
|---|---|---|---|---|
| List job's applications | `GET` | `/api/job-postings/<job_id>/applications` | Returns all applications submitted for this job | `200 OK` |
| Apply to job posting | `POST` | `/api/job-postings/<job_id>/applications` | Submits an application for this specific job | `201 Created` |

#### API Error Responses

| Status Code | Condition |
|---|---|
| `400 Bad Request` | Missing required fields (`title`, `company`, `employment_type`, or `salary_range`) or `title` exceeding 120 characters |
| `404 Not Found` | No job posting found with the given `id` |

---

### Postman — Form-Data Examples

**POST /api/job-postings/** — Create a full-time job posting

| Key | Value |
|---|---|
| `title` | Backend Developer |
| `company` | TechCorp Istanbul |
| `city` | Istanbul |
| `description` | We are looking for a Python/Flask backend developer with 2+ years of experience. |
| `employment_type` | full-time |
| `salary_range` | 25.000-40.000 TL |
| `posted_by` | hr@techcorp.com |
| `is_active` | true |
| `expires_at` | 2025-12-31 |

**POST /api/job-postings/** — Create an internship posting

| Key | Value |
|---|---|
| `title` | Summer Internship — Data Analyst |
| `company` | DataWorks |
| `city` | Remote |
| `description` | 3-month summer internship for students in their 3rd or 4th year. |
| `employment_type` | internship |
| `salary_range` | 15.000-20.000 TL |
| `posted_by` | careers@dataworks.com |

**PATCH /api/job-postings/1** — Deactivate a job posting

| Key | Value |
|---|---|
| `is_active` | false |

**PUT /api/job-postings/1** — Full replace (all required fields)

| Key | Value |
|---|---|
| `title` | Senior Backend Developer |
| `company` | TechCorp Istanbul |
| `city` | Istanbul / Hybrid |
| `description` | Updated: Now seeking a senior-level developer with 5+ years of experience. |
| `employment_type` | full-time |
| `salary_range` | 40.000-60.000 TL |
| `posted_by` | hr@techcorp.com |
| `is_active` | true |
| `expires_at` | 2026-03-31 |

---

## Application

**Model file:** [`app/models/application.py`](app/models/application.py)  
**Storage:** Database via SQLAlchemy & Flask-Migrate (PostgreSQL in Docker / SQLite fallback)  
**Controllers:** `ApplicationController` (HTML) · `ApiApplicationController` (JSON API)

> **Action Table Role:** `Application` tablosu `User` ve `JobPosting` modelleri arasındaki **Eylem Tablosudur (Action / Junction Table)**. `users` ile `job_postings` arasında doğrudan FK ilişkisi bulunmaz; kullanıcıların ilanlarla etkileşimi (başvuru yapma) bu tablo üzerinden yürütülür.

### Field Definitions

| Field | Python Type | DB Type | Form Field (`name=`) | Required | Default | Notes |
|---|---|---|---|---|---|---|
| `id` | `int` | `Integer` PK | — | — | Auto-increment | Assigned by the model on create; not sent in form |
| `user_id` | `int` | `Integer` FK | `user_id` | Yes | — | FK → `users.id`; links application to the applicant user |
| `job_posting_id` | `int` | `Integer` FK | `job_posting_id` | Yes | — | FK → `job_postings.id`; links application to the job posting |
| `resume_url` | `str` | `String(255)` | `resume_url` | No | `None` | Link to CV, LinkedIn, or portfolio |
| `cover_letter` | `str` | `Text` | `cover_letter` | No | `None` | Candidate's message / statement of interest |
| `status` | `str` | `String(50)` | `status` | No | `"pending"` | Accepted: `pending`, `reviewed`, `accepted`, `rejected` |
| `applied_at` | `str` | `String(30)` | — | — | `datetime.now()` | Set automatically on application creation; not editable |

### Relationships

| Relationship | Type | Target Model | Foreign Key | Notes |
|---|---|---|---|---|
| `user` | Many-to-One | `User` | `applications.user_id → users.id` | The applicant user |
| `job_posting` | Many-to-One | `JobPosting` | `applications.job_posting_id → job_postings.id` | The target job posting |

### Business Rules

- `user_id` and `job_posting_id` are required on both `POST` (create) and `PUT` (full update).
- Both `user_id` and `job_posting_id` must refer to existing records in the database.
- `status` defaults to `"pending"` if not provided; valid values: `pending`, `reviewed`, `accepted`, `rejected`.
- `applied_at` is set once at creation time and never modified.
- `id` is never accepted from the client; it is always assigned server-side.

---

### CRUD Operations

#### Web Interface (HTML)

| Operation | Method | URL | Controller Method | View Template |
|---|---|---|---|---|
| List all | `GET` | `/applications/` | `ApplicationController.index()` | `application/index.html` |
| Show create form | `GET` | `/applications/new` | — | `application/create.html` |
| Create | `POST` | `/applications/` | `ApplicationController.create(data)` | Redirects to list on success |
| Show edit form | `GET` | `/applications/<id>/edit` | `ApplicationController.show(id)` | `application/edit.html` |
| Update | `POST` | `/applications/<id>/edit` | `ApplicationController.update(id, data)` | Redirects to list on success |
| Delete | `POST` | `/applications/<id>/delete` | `ApplicationController.delete(id)` | Redirects to list on success |

#### REST API (JSON)

| Operation | Method | URL | Controller Method | Success Code |
|---|---|---|---|---|
| List all | `GET` | `/api/applications/` | `ApiApplicationController.index()` | `200 OK` |
| Get by ID | `GET` | `/api/applications/<id>` | `ApiApplicationController.show(id)` | `200 OK` |
| Create | `POST` | `/api/applications/` | `ApiApplicationController.create()` | `201 Created` |
| Full update | `PUT` | `/api/applications/<id>` | `ApiApplicationController.update(id)` | `200 OK` |
| Partial update | `PATCH` | `/api/applications/<id>` | `ApiApplicationController.partial_update(id)` | `200 OK` |
| Delete | `DELETE` | `/api/applications/<id>` | `ApiApplicationController.delete(id)` | `200 OK` |

#### API Error Responses

| Status Code | Condition |
|---|---|
| `400 Bad Request` | Missing `user_id` or `job_posting_id` |
| `404 Not Found` | No application found with the given `id`, or referenced `user`/`job_posting` not found |

---

### Postman — Form-Data Examples

**POST /api/applications/** — Submit a new job application

| Key | Value |
|---|---|
| `user_id` | 1 |
| `job_posting_id` | 1 |
| `resume_url` | https://linkedin.com/in/example |
| `cover_letter` | I have strong experience in Python and Flask backend architectures. |
| `status` | pending |

**PATCH /api/applications/1** — Update application status

| Key | Value |
|---|---|
| `status` | reviewed |

**PUT /api/applications/1** — Full replace

| Key | Value |
|---|---|
| `user_id` | 1 |
| `job_posting_id` | 1 |
| `resume_url` | https://github.com/example/cv.pdf |
| `cover_letter` | Updated cover letter with additional project details. |
| `status` | accepted |

---

## Middleware & Error Handling

### 1. Terminal Request Logger (`app/middleware/logger.py`)
Prints a single summary line per HTTP request to stdout:

```text
time        method   route                           status  duration
10:20:30    POST     /api/users                      201     18ms
```

### 2. 404 Guardian & Generic `/404` Page (`app/middleware/not_found_guardian.py`)
Catches all `404 Not Found` errors across the application:

| Request Target | Behavior | Response |
|---|---|---|
| `/api/*` | Returns JSON with `reason` and close-match route `suggestions` | `404 Not Found` (`application/json`) |
| Web / HTML routes | Redirects (`302`) to `/404?path=<path>&reason=<reason>` | `302 Found` → `GET /404` (`404 Not Found` HTML via `templates/404.html`) |

### 3. 5xx Server Error Guardian (`app/middleware/server_error_guardian.py`)
Catches `500–504` HTTP errors and any unhandled runtime exceptions:

| Request Target | Behavior | Response |
|---|---|---|
| `/api/*` | Returns JSON with `code`, `reason`, `error_type`, `method`, and `path` | `500 Internal Server Error` (`application/json`) |
| Web / HTML routes | Renders an HTML error page displaying `code`, `reason`, and `error_type` | `500 Internal Server Error` (`text/html`) |

### 4. Error File Logger (`app/middleware/error_log.py`)
Appends all `404` and `5xx` errors (including full stack traces for `5xx`) to `logs/error.logs`:

```text
2026-11-11 10:38:48 | 404 | GET    | /api/job-postingz | No route matches '/api/job-postingz'. The URL does not exist on this server.
2026-11-11 10:38:48 | 500 | GET    | /api/debug/500 | RuntimeError: Intentional test error triggered from /debug/500
```

---

## Swagger / OpenAPI

Interactive API documentation is available at:

```
http://localhost:5000/api/swagger
```

All `/api/users`, `/api/announcements`, `/api/job-postings`, and `/api/applications` endpoints are documented there with request parameters and response schemas.
