"""
AnnouncementFactory — generates realistic mock Announcement records for development and testing.
"""

import random
from faker import Faker
from app.models.announcement import Announcement

fake = Faker(["tr_TR", "en_US"])

SAMPLE_ANNOUNCEMENTS = [
    {
        "title": "Annual Alumni Reunion 2026",
        "content": "Join us on campus this June for networking, speeches, and reconnection with fellow graduates.",
        "author": "Alumni Relations Office",
    },
    {
        "title": "Spring Career & Internship Fair",
        "content": "Over 50 companies will be visiting the campus sports hall to meet students and recent graduates.",
        "author": "Career Center",
    },
    {
        "title": "Mentorship Program Applications Open",
        "content": "Experienced alumni can now sign up to mentor current 3rd and 4th-year students for the upcoming term.",
        "author": "Mentorship Committee",
    },
    {
        "title": "Guest Speaker: Artificial Intelligence in Modern Software",
        "content": "Distinguished alumnus Dr. Emre Demir will deliver a keynote on modern AI pipelines next Wednesday.",
        "author": "Faculty of Engineering",
    },
    {
        "title": "Startup Pitch Competition - Seed Funding",
        "content": "Alumni and students with startup ideas are invited to apply for the annual venture seed grant.",
        "author": "Innovation & Incubation Hub",
    },
    {
        "title": "Graduate Scholarship Announcement",
        "content": "Applications are open for postgraduate academic excellence scholarships funded by alumni donors.",
        "author": "Dean of Students",
    },
]


class AnnouncementFactory:
    """Factory class for generating Announcement model instances."""

    @classmethod
    def build(cls, **overrides) -> dict:
        """
        Builds raw announcement dictionary data without persisting to the database.
        """
        template = random.choice(SAMPLE_ANNOUNCEMENTS)

        data = {
            "title": template["title"] if random.random() < 0.7 else f"{fake.sentence(nb_words=5)}",
            "content": template["content"] if random.random() < 0.7 else fake.paragraph(nb_sentences=3),
            "author": template["author"] if random.random() < 0.7 else f"{fake.name()} ({fake.job()})",
            "is_active": overrides.get("is_active", True if random.random() > 0.15 else False),
        }
        data.update(overrides)
        return data

    @classmethod
    def create(cls, **overrides) -> Announcement:
        """
        Builds and persists a new Announcement in the database.
        """
        data = cls.build(**overrides)
        return Announcement.create(data)

    @classmethod
    def create_batch(cls, count: int = 5, **overrides) -> list[Announcement]:
        """
        Creates multiple Announcement records in the database.
        """
        return [cls.create(**overrides) for _ in range(count)]
