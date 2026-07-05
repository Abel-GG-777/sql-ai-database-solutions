from __future__ import annotations

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_DB_PATH = DATA_DIR / "sample.db"
SEED_SQL_PATH = DATA_DIR / "seed_data.sql"


def get_connection(db_path: Path | str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Open a SQLite connection with dictionary-like row access."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def ensure_database(db_path: Path | str = DEFAULT_DB_PATH) -> Path:
    """Create the sample SQLite database from seed_data.sql when needed."""
    db_path = Path(db_path)
    if db_path.exists():
        return db_path

    if not SEED_SQL_PATH.exists():
        raise FileNotFoundError(f"Seed file not found: {SEED_SQL_PATH}")

    db_path.parent.mkdir(parents=True, exist_ok=True)
    seed_sql = SEED_SQL_PATH.read_text(encoding="utf-8")

    with get_connection(db_path) as connection:
        connection.executescript(seed_sql)

    return db_path


def reset_database(db_path: Path | str = DEFAULT_DB_PATH) -> Path:
    """Recreate a database from the seed script. Intended for tests and demos."""
    db_path = Path(db_path)
    if db_path.exists():
        db_path.unlink()
    return ensure_database(db_path)
