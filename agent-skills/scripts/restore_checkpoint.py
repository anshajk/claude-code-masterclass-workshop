"""Restore skill development checkpoints for the Agent Skills masterclass."""
import shutil
import sys
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parents[1]
CHECKPOINTS_DIR = DEMO_ROOT / "checkpoints"
SKILLS_DIR = DEMO_ROOT / ".claude" / "skills"


def restore(checkpoint: str):
    source = CHECKPOINTS_DIR / checkpoint / ".claude" / "skills"
    if not source.exists():
        valid = ", ".join(p.name for p in sorted(CHECKPOINTS_DIR.iterdir()) if p.is_dir())
        raise SystemExit(f"Unknown checkpoint {checkpoint!r}. Choose one of: {valid}")

    for skill_name in ("change-risk-review", "safe-sqlite-migrations"):
        skill_target = SKILLS_DIR / skill_name
        if skill_target.exists():
            shutil.rmtree(skill_target)

    skill_target = SKILLS_DIR / "safe-sqlite-migrations"
    src_skill = source / "safe-sqlite-migrations"
    if src_skill.exists():
        shutil.copytree(src_skill, skill_target)
        print(f"Restored checkpoint: {checkpoint} (copied {skill_target})")
    else:
        SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Restored checkpoint: {checkpoint} (clean .claude/skills/ directory)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/restore_checkpoint.py <starter | basic-skill | complete-skill>")
        sys.exit(1)

    restore(sys.argv[1].lower())
