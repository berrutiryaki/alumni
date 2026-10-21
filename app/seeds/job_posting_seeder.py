"""
JobPostingSeeder — seeds the database with initial and fake JobPosting records.
"""

from app.models.job_posting import JobPosting
from app.factories.job_posting_factory import JobPostingFactory, SAMPLE_JOB_POSTINGS


class JobPostingSeeder:

    @classmethod
    def run(cls, extra_count: int = 4):
        print("[*] Seeding Job Postings...")

        # 1. Seed known sample job postings if empty or low
        if JobPosting.query.count() == 0:
            for item in SAMPLE_JOB_POSTINGS:
                jp = JobPostingFactory.create(
                    title=item["title"],
                    company=item["company"],
                    description=item["description"],
                    location=item["location"],
                    employment_type=item["employment_type"],
                    salary_range=item["salary_range"],
                    posted_by=item["posted_by"],
                    expires_at=item["expires_at"],
                    is_active=True,
                )
                print(f"    + Job: {jp.title} at {jp.company} ({jp.employment_type})")

        # 2. Seed additional randomized job postings via factory
        for _ in range(extra_count):
            jp = JobPostingFactory.create()
            print(f"    + Job: {jp.title} at {jp.company} ({'Active' if jp.is_active else 'Inactive'})")

        print(f"[OK] Successfully seeded {JobPosting.query.count()} total job postings.")
