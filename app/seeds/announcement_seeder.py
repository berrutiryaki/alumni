"""
AnnouncementSeeder — seeds the database with initial and fake Announcement records.
"""

from app.models.announcement import Announcement
from app.factories.announcement_factory import AnnouncementFactory, SAMPLE_ANNOUNCEMENTS


class AnnouncementSeeder:

    @classmethod
    def run(cls, extra_count: int = 4):
        print(f"[*] Seeding Announcements...")

        # 1. Seed known high-quality sample announcements if empty
        if Announcement.query.count() == 0:
            for item in SAMPLE_ANNOUNCEMENTS[:4]:
                a = Announcement.create({
                    "title": item["title"],
                    "content": item["content"],
                    "author": item["author"],
                    "is_active": True,
                })
                print(f"    + Announcement: {a.title}")

        # 2. Seed additional randomized announcements via factory
        for _ in range(extra_count):
            a = AnnouncementFactory.create()
            print(f"    + Announcement: {a.title} ({'Active' if a.is_active else 'Inactive'})")

        print(f"[OK] Successfully seeded {Announcement.query.count()} total announcements.")
