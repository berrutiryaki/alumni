"""
DatabaseSeeder — orchestrates all model seeders.
"""

from app.database import db
from app.models.user import User
from app.models.announcement import Announcement
from app.models.job_posting import JobPosting
from app.models.application import Application
from app.seeds.user_seeder import UserSeeder
from app.seeds.announcement_seeder import AnnouncementSeeder
from app.seeds.job_posting_seeder import JobPostingSeeder


class DatabaseSeeder:

    @classmethod
    def run(cls, clean: bool = False, student_count: int = 10, alumni_count: int = 10,
            announcement_count: int = 4, job_posting_count: int = 4):
        """
        Runs all seeders within the application database context.

        Args:
            clean: If True, clears existing records before seeding.
        """
        print("=" * 60)
        print("STARTING DATABASE SEEDING PROCESS")
        print("=" * 60)

        if clean:
            print("[*] Cleaning existing database records...")
            Application.query.delete()
            JobPosting.query.delete()
            Announcement.query.delete()
            User.query.delete()
            db.session.commit()
            print("[OK] Database cleared.")

        UserSeeder.run(student_count=student_count, alumni_count=alumni_count)
        print("-" * 60)
        AnnouncementSeeder.run(extra_count=announcement_count)
        print("-" * 60)
        JobPostingSeeder.run(extra_count=job_posting_count)

        print("=" * 60)
        print("SEEDING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
