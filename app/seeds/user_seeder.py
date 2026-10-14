"""
UserSeeder — seeds the database with initial and fake User records.
"""

from app.models.user import User
from app.factories.user_factory import UserFactory


class UserSeeder:

    @classmethod
    def run(cls, student_count: int = 10, alumni_count: int = 10):
        print(f"[*] Seeding Users ({student_count} students, {alumni_count} alumni)...")

        # 1. Fixed demo records if not already existing
        demo_users = [
            {
                "name": "Berru Tiryaki",
                "email": "berru@example.com",
                "status": "alumni",
                "department": "Computer Engineering",
                "graduation_year": 2024,
            },
            {
                "name": "Ahmet Yilmaz",
                "email": "ahmet@example.com",
                "status": "student",
                "department": "Software Engineering",
                "graduation_year": None,
            },
            {
                "name": "Zeynep Kaya",
                "email": "zeynep@example.com",
                "status": "alumni",
                "department": "Business Administration",
                "graduation_year": 2021,
            },
        ]

        for demo in demo_users:
            existing = User.query.filter_by(email=demo["email"]).first()
            if not existing:
                User.create(demo)
                print(f"    + Created demo user: {demo['name']} ({demo['email']})")

        # 2. Seed random students
        for _ in range(student_count):
            u = UserFactory.create_student()
            print(f"    + Student: {u.name} - {u.department}")

        # 3. Seed random alumni
        for _ in range(alumni_count):
            u = UserFactory.create_alumni()
            print(f"    + Alumni: {u.name} - {u.department} ('{str(u.graduation_year)[-2:]})")

        print(f"[OK] Successfully seeded {User.query.count()} total users.")
