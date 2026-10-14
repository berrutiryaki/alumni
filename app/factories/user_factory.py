"""
UserFactory — generates realistic mock User records for development and testing.
"""

import random
from faker import Faker
from app.models.user import User

fake = Faker(["tr_TR", "en_US"])

DEPARTMENTS = [
    "Computer Engineering",
    "Software Engineering",
    "Electrical & Electronics Engineering",
    "Industrial Engineering",
    "Mechanical Engineering",
    "Business Administration",
    "Economics",
    "Architecture",
    "Law",
    "Medicine",
]


class UserFactory:
    """Factory class for generating User model instances."""

    @classmethod
    def build(cls, **overrides) -> dict:
        """
        Builds raw user dictionary data without persisting to the database.
        """
        first_name = fake.first_name()
        last_name = fake.last_name()
        name = f"{first_name} {last_name}"

        # Clean email generation to avoid duplicate collisions
        email_prefix = f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 9999)}"
        clean_email = (
            email_prefix.replace("ç", "c")
            .replace("ğ", "g")
            .replace("ı", "i")
            .replace("ö", "o")
            .replace("ş", "s")
            .replace("ü", "u")
            .replace(" ", "")
            + "@example.com"
        )

        status = overrides.get("status") or random.choice(["student", "alumni"])
        graduation_year = None
        if status == "alumni":
            graduation_year = overrides.get("graduation_year") or random.randint(2010, 2024)

        data = {
            "name": name,
            "email": clean_email,
            "status": status,
            "department": random.choice(DEPARTMENTS),
            "graduation_year": graduation_year,
        }
        data.update(overrides)
        return data

    @classmethod
    def create(cls, **overrides) -> User:
        """
        Builds and persists a new User in the database.
        """
        data = cls.build(**overrides)
        return User.create(data)

    @classmethod
    def create_student(cls, **overrides) -> User:
        """
        Helper to create a student specifically.
        """
        overrides["status"] = "student"
        overrides["graduation_year"] = None
        return cls.create(**overrides)

    @classmethod
    def create_alumni(cls, graduation_year: int = None, **overrides) -> User:
        """
        Helper to create an alumni specifically.
        """
        overrides["status"] = "alumni"
        if graduation_year:
            overrides["graduation_year"] = graduation_year
        elif "graduation_year" not in overrides:
            overrides["graduation_year"] = random.randint(2010, 2024)
        return cls.create(**overrides)

    @classmethod
    def create_batch(cls, count: int = 5, **overrides) -> list[User]:
        """
        Creates multiple User records in the database.
        """
        return [cls.create(**overrides) for _ in range(count)]
