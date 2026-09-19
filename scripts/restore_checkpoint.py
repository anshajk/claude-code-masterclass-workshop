from pathlib import Path
import shutil
import sys


DEMO_ROOT = Path(__file__).resolve().parents[1]
CHECKPOINTS = DEMO_ROOT / "checkpoints"
TARGETS = (
    Path("workshop_agent/agent.py"),
    Path("workshop_agent/tools.py"),
    Path("tests/test_tools.py"),
)


def restore(name: str) -> None:
    source = CHECKPOINTS / name
    if not source.is_dir():
        choices = ", ".join(path.name for path in sorted(CHECKPOINTS.iterdir()))
        raise SystemExit(f"Unknown checkpoint {name!r}. Choose one of: {choices}")

    for target_name in TARGETS:
        source_target = source / target_name
        target = DEMO_ROOT / target_name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_target, target)

    print(f"Restored checkpoint: {name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/restore_checkpoint.py CHECKPOINT")
    restore(sys.argv[1])
