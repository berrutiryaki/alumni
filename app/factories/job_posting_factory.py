"""
JobPostingFactory — generates realistic mock JobPosting records for development and testing.
"""

import random
from faker import Faker
from app.models.job_posting import JobPosting

fake = Faker(["tr_TR", "en_US"])

SAMPLE_JOB_POSTINGS = [
    {
        "title": "Backend Python / Flask Developer",
        "company": "Trendyol Group",
        "description": "Looking for a backend developer with solid experience in Python, Flask, SQLAlchemy, and relational databases. Docker and CI/CD knowledge is a plus.",
        "location": "Istanbul / Hybrid",
        "employment_type": "full-time",
        "salary_range": "65.000 - 90.000 TL",
        "posted_by": "talent@trendyol.com",
        "expires_at": "2026-12-31",
    },
    {
        "title": "Data Science & AI Intern",
        "company": "Getir",
        "description": "Summer internship for 3rd and 4th-year computer engineering or mathematics students. Work with machine learning models and data pipelines.",
        "location": "Istanbul / Remote",
        "employment_type": "internship",
        "salary_range": "25.000 - 35.000 TL",
        "posted_by": "campus@getir.com",
        "expires_at": "2026-08-31",
    },
    {
        "title": "DevOps & Cloud Infrastructure Engineer",
        "company": "Hepsiburada",
        "description": "Managing Kubernetes clusters, automated deployments, monitoring, and infrastructure on AWS/GCP.",
        "location": "Remote",
        "employment_type": "full-time",
        "salary_range": "80.000 - 120.000 TL",
        "posted_by": "careers@hepsiburada.com",
        "expires_at": "2026-11-30",
    },
    {
        "title": "Frontend React Developer",
        "company": "Insider",
        "description": "Seeking a frontend developer proficient in React, TypeScript, responsive UI development, and RESTful API integration.",
        "location": "Istanbul",
        "employment_type": "full-time",
        "salary_range": "60.000 - 85.000 TL",
        "posted_by": "hr@useinsider.com",
        "expires_at": "2026-10-15",
    },
    {
        "title": "Junior Mobile Developer (Flutter / React Native)",
        "company": "Papara",
        "description": "Join our mobile payments engineering team. Fresh graduates and recent alumni are strongly encouraged to apply.",
        "location": "Istanbul / Hybrid",
        "employment_type": "full-time",
        "salary_range": "50.000 - 70.000 TL",
        "posted_by": "jobs@papara.com",
        "expires_at": "2026-09-30",
    },
    {
        "title": "Part-Time QA Automation Tester",
        "company": "Peak Games",
        "description": "Part-time opportunity for students: automated regression tests, test suites, and bug reporting in a fast-paced environment.",
        "location": "Remote",
        "employment_type": "part-time",
        "salary_range": "30.000 - 45.000 TL",
        "posted_by": "qa-leads@peak.com",
        "expires_at": "2026-07-31",
    },
]


class JobPostingFactory:
    """Factory class for generating JobPosting model instances."""

    @classmethod
    def build(cls, **overrides) -> dict:
        """Builds raw job posting dictionary data without persisting to the database."""
        template = random.choice(SAMPLE_JOB_POSTINGS)

        employment_types = ["full-time", "part-time", "internship", "contract", "remote"]

        tech_roles = [
            "Senior Backend Engineer (Python)", "Data Engineer", "Cloud Solutions Architect",
            "Full Stack Developer (React & Node.js)", "Mobile iOS Developer (Swift)",
            "Product Designer (UI/UX)", "Cybersecurity Specialist", "Machine Learning Researcher",
            "Junior DevOps Engineer", "Product Manager"
        ]

        data = {
            "title": template["title"] if random.random() < 0.6 else random.choice(tech_roles),
            "company": template["company"] if random.random() < 0.7 else fake.company(),
            "description": template["description"] if random.random() < 0.6 else fake.paragraph(nb_sentences=4),
            "location": template["location"] if random.random() < 0.7 else f"{fake.city()} / Remote",
            "employment_type": overrides.get("employment_type", template.get("employment_type", random.choice(employment_types))),
            "salary_range": template.get("salary_range", "Competitive"),
            "posted_by": template.get("posted_by") if random.random() < 0.7 else fake.company_email(),
            "is_active": overrides.get("is_active", True if random.random() > 0.1 else False),
            "expires_at": template.get("expires_at", "2026-12-31"),
        }
        data.update(overrides)
        return data

    @classmethod
    def create(cls, **overrides) -> JobPosting:
        """Builds and persists a new JobPosting in the database."""
        data = cls.build(**overrides)
        return JobPosting.create(data)

    @classmethod
    def create_batch(cls, count: int = 5, **overrides) -> list[JobPosting]:
        """Creates multiple JobPosting records in the database."""
        return [cls.create(**overrides) for _ in range(count)]
