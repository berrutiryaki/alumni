"""
DatabaseSeeder — orchestrates all model seeders.
"""

from app.database import db
from app.models.user import User
from app.models.announcement import Announcement
from app.seeds.user_seeder import UserSeeder
from app.seeds.announcement_seeder import AnnouncementSeeder


class DatabaseSeeder:

    @classmethod
    def run(cls, clean: bool = False, student_count: int = 10, alumni_count: int = 10, announcement_count: int = 4):
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
            Announcement.query.delete()
            User.query.delete()
            db.session.commit()
            print("[OK] Database cleared.")

        UserSeeder.run(student_count=student_count, alumni_count=alumni_count)
        print("-" * 60)
        AnnouncementSeeder.run(extra_count=announcement_count)

        print("=" * 60)
        print("SEEDING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
