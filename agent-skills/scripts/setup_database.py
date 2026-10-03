"""Create a fresh local SQLite database for the workshop."""

import argparse
import sqlite3
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = DEMO_ROOT / "database" / "schema.sql"
SEED_PATH = DEMO_ROOT / "database" / "seed.sql"
DEFAULT_DATABASE = DEMO_ROOT / "workshop.db"


def create_database(database: Path) -> None:
    database.parent.mkdir(parents=True, exist_ok=True)
    database.unlink(missing_ok=True)

    with sqlite3.connect(database) as connection:
        connection.executescript(SCHEMA_PATH.read_text())
        connection.executescript(SEED_PATH.read_text())
        connection.execute("PRAGMA foreign_keys = ON")
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {integrity}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("database", nargs="?", type=Path, default=DEFAULT_DATABASE)
    args = parser.parse_args()
    database = args.database.resolve()
    create_database(database)
    print(f"Created {database}")


if __name__ == "__main__":
    main()
