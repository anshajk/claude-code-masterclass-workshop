import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.setup_database import create_database

DEMO_ROOT = Path(__file__).resolve().parents[1]
GUARD = (
    DEMO_ROOT
    / "checkpoints"
    / "complete-skill"
    / ".claude"
    / "skills"
    / "safe-sqlite-migrations"
    / "scripts"
    / "sqlite_guard.py"
)


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "workshop.db"
    create_database(path)
    return path


def run_guard(*args):
    return subprocess.run(
        [sys.executable, str(GUARD), *map(str, args)],
        capture_output=True,
        text=True,
    )


def test_seeded_database_contains_query_examples(database):
    with sqlite3.connect(database) as connection:
        no_orders = connection.execute(
            "SELECT name FROM customers WHERE active = 1 AND NOT EXISTS "
            "(SELECT 1 FROM orders WHERE orders.customer_id = customers.id)"
        ).fetchall()
        mismatched = connection.execute(
            "SELECT orders.id FROM orders JOIN order_items ON order_items.order_id = orders.id "
            "GROUP BY orders.id HAVING orders.total_cents != "
            "SUM(order_items.quantity * order_items.unit_price_cents)"
        ).fetchall()

    assert no_orders == [("Curious Labs",)]
    assert mismatched == [(103,)]


def test_query_mode_rejects_writes(database):
    original = database.read_bytes()
    result = run_guard("query", database, "--sql", "DELETE FROM customers")
    assert result.returncode == 1
    assert "readonly" in result.stderr.lower()
    assert database.read_bytes() == original

    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 4


@pytest.mark.parametrize(
    ("scenario", "returncode", "message"),
    [
        ("01-add-order-status.sql", 0, "SAFE"),
        ("02-required-customer-phone.sql", 1, "UNSAFE"),
        ("03-drop-legacy-note.sql", 2, "NEEDS REVIEW"),
    ],
)
def test_migration_scenarios_use_disposable_copy(database, scenario, returncode, message):
    original = database.read_bytes()
    result = run_guard(
        "validate",
        database,
        DEMO_ROOT / "scenarios" / scenario,
    )
    assert result.returncode == returncode
    assert message in result.stdout
    assert database.read_bytes() == original

    with sqlite3.connect(database) as connection:
        columns = {
            row[1] for row in connection.execute("PRAGMA table_info(orders)").fetchall()
        }
    assert columns == {"id", "customer_id", "ordered_at", "total_cents", "legacy_note"}
