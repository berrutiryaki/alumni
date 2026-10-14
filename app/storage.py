"""
JSONStore — lightweight file-based persistence helper.

Saves and loads model data as JSON files to/from a configurable
data directory. Used by models until PostgreSQL is integrated.

The data directory is controlled by the DATA_DIR environment variable
(defaults to ./data relative to the project root).
"""

import json
import os
from pathlib import Path


DATA_DIR = Path(os.environ.get("DATA_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")))


def _path(filename: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR / filename


def load(filename: str) -> list:
    """Load a list from a JSON file. Returns empty list if file does not exist."""
    p = _path(filename)
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save(filename: str, data: list) -> None:
    """Persist a list to a JSON file."""
    with open(_path(filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
