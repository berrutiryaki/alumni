"""
ApplicationFactory — generates realistic mock Application records for development and testing.
Connects users (applicants) to job postings as an Action Table.
"""

import random
from faker import Faker
from app.models.application import Application
from app.models.user import User
from app.models.job_posting import JobPosting

fake = Faker(["tr_TR", "en_US"])

SAMPLE_COVER_LETTERS = [
    "I have been following your team's engineering blog and open-source contributions with great admiration. With my hands-on background in modern backend architectures and distributed systems, I am eager to contribute immediately to your production services.",
    "As a recent graduate in Computer Engineering, I am excited about the opportunity to apply my knowledge of Python, REST APIs, and database design. I have built several projects utilizing Flask and PostgreSQL, which align well with this position.",
    "I believe my background in frontend engineering with React and TypeScript makes me a strong match for this role. I have previously developed responsive web applications and collaborated closely with product managers and backend engineers.",
    "Having completed an intensive internship focused on data engineering and machine learning workflows, I am very keen on joining your data analytics team. I look forward to contributing to your data pipelines.",
    "Merhabalar, şirketinizin vizyonunu ve teknolojik altyapısını uzun süredir takip etmekteyim. Üniversite sürecinde geliştirdiğim projeler ve staj deneyimlerim doğrultusunda bu pozisyona değer katabileceğime inanıyorum.",
    "Yazılım mühendisliği mezuniyetim sonrasında özellikle mobil uygulama geliştirme ve modern web teknolojileri üzerine yoğunlaştım. Ekibinizle birlikte yenilikçi ürünler geliştirmekten büyük mutluluk duyarım.",
    "I am writing to express my strong enthusiasm for this internship position. I am eager to learn from experienced engineers and take on challenging real-world tasks in a fast-paced environment.",
    "With over 3 years of hands-on experience in cloud infrastructure, container orchestration, and CI/CD pipelines, I am confident in my ability to help streamline your deployment processes."
]

SAMPLE_STATUSES = ["pending", "pending", "pending", "reviewed", "reviewed", "accepted", "rejected"]


class ApplicationFactory:
    """Factory class for generating Application model instances."""

    @classmethod
    def build(cls, **overrides) -> dict:
        """
        Builds raw application dictionary data without persisting to the database.
        """
        user_id = overrides.get("user_id")
        if not user_id:
            users = User.query.all()
            if users:
                user_id = random.choice(users).id
            else:
                user_id = 1

        job_posting_id = overrides.get("job_posting_id")
        if not job_posting_id:
            jobs = JobPosting.query.all()
            if jobs:
                job_posting_id = random.choice(jobs).id
            else:
                job_posting_id = 1

        username = fake.user_name().lower()
        resume_options = [
            f"https://linkedin.com/in/{username}",
            f"https://github.com/{username}",
            f"https://drive.google.com/file/d/{fake.uuid4()}/view",
            f"https://portfolio.{username}.dev/cv.pdf",
            None
        ]

        data = {
            "user_id": user_id,
            "job_posting_id": job_posting_id,
            "resume_url": overrides.get("resume_url", random.choice(resume_options)),
            "cover_letter": overrides.get("cover_letter", random.choice(SAMPLE_COVER_LETTERS)),
            "status": overrides.get("status", random.choice(SAMPLE_STATUSES)),
        }
        data.update(overrides)
        return data

    @classmethod
    def create(cls, **overrides) -> Application:
        """
        Builds and persists a new Application in the database.
        """
        data = cls.build(**overrides)
        return Application.create(data)

    @classmethod
    def create_batch(cls, count: int = 5, **overrides) -> list[Application]:
        """
        Creates multiple Application records in the database.
        """
        return [cls.create(**overrides) for _ in range(count)]
