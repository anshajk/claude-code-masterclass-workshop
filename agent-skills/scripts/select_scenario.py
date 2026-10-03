"""Select or reset a migration scenario for the workshop."""

import shutil
import sys
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_DIR = DEMO_ROOT / "scenarios"
CURRENT_MIGRATION = DEMO_ROOT / "migrations" / "current.sql"


def select_scenario(name: str) -> None:
    matches = sorted(SCENARIOS_DIR.glob(f"*{name}*.sql"))
    if len(matches) != 1:
        available = "\n  ".join(path.stem for path in sorted(SCENARIOS_DIR.glob("*.sql")))
        raise SystemExit(f"Scenario {name!r} is ambiguous or missing. Available:\n  {available}")

    CURRENT_MIGRATION.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(matches[0], CURRENT_MIGRATION)
    print(f"Selected {matches[0].stem} -> {CURRENT_MIGRATION.relative_to(DEMO_ROOT)}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/select_scenario.py <1 | 2 | 3 | reset>")

    name = sys.argv[1].lower()
    if name == "reset":
        CURRENT_MIGRATION.unlink(missing_ok=True)
        print("Removed migrations/current.sql")
    else:
        select_scenario(name)


if __name__ == "__main__":
    main()
