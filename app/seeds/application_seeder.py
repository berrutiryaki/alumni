"""
ApplicationSeeder — seeds the database with realistic Application records connecting users and job postings.
"""

import random
from app.models.application import Application
from app.models.user import User
from app.models.job_posting import JobPosting
from app.factories.application_factory import ApplicationFactory


class ApplicationSeeder:

    @classmethod
    def run(cls, count: int = 10):
        print("[*] Seeding Applications...")

        users = User.query.all()
        jobs = JobPosting.query.filter_by(is_active=True).all()

        if not jobs:
            jobs = JobPosting.query.all()

        if not users or not jobs:
            print("    [!] Cannot seed applications: Users or JobPostings table is empty.")
            return

        # Keep track of existing (user_id, job_posting_id) pairs to avoid duplicates
        existing_pairs = {
            (app.user_id, app.job_posting_id)
            for app in Application.query.with_entities(Application.user_id, Application.job_posting_id).all()
        }

        # Select a diverse set of users (students and alumni)
        shuffled_users = list(users)
        random.shuffle(shuffled_users)

        created_count = 0
        statuses = ["pending", "reviewed", "accepted", "rejected"]
        status_weights = [4, 3, 2, 1]

        for user in shuffled_users:
            if created_count >= count:
                break

            # Pick 1 or 2 distinct jobs for this user
            candidate_jobs = [j for j in jobs if (user.id, j.id) not in existing_pairs]
            if not candidate_jobs:
                continue

            # Pick a job
            chosen_job = random.choice(candidate_jobs)
            status = random.choices(statuses, weights=status_weights, k=1)[0]

            app_rec = ApplicationFactory.create(
                user_id=user.id,
                job_posting_id=chosen_job.id,
                status=status
            )
            existing_pairs.add((user.id, chosen_job.id))
            created_count += 1
            print(f"    + Application: {user.name} -> {chosen_job.title} @ {chosen_job.company} [{status.upper()}]")

        print(f"[OK] Successfully seeded {Application.query.count()} total applications across multiple users.")
