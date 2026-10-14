"""
seed.py — Command-line runner for database seeding.

Usage:
    python seed.py          # Seeds sample records
    python seed.py --clean  # Clears existing records first, then seeds
"""

import sys
from run import app
from app.seeds.database_seeder import DatabaseSeeder

if __name__ == "__main__":
    clean_flag = "--clean" in sys.argv
    with app.app_context():
        DatabaseSeeder.run(clean=clean_flag)
