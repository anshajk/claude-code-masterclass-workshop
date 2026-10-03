# Agent Skills Workshop: `safe-sqlite-migrations`

Hands-on companion project for the Ergosphere Labs masterclass: **Agent Skills: From Repeated Prompt to Reusable Capability**.

In this exercise, you will build, invoke, test, and harden a `safe-sqlite-migrations` skill. It inspects a local SQLite database, answers targeted read-only questions, and validates migrations against a disposable copy.

## Environment Setup

Requires Python 3.10+ and Git:

```sh
git clone https://github.com/anshajk/claude-code-masterclass-workshop.git
cd claude-code-masterclass-workshop/agent-skills
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
python scripts/setup_database.py
```

## Workshop Workflow

### Phase 1: Create the Minimum Portable Skill (Stage A & B)
Create `.claude/skills/safe-sqlite-migrations/SKILL.md` with:
- Frontmatter: `name` and trigger-focused `description`
- A read-only query boundary
- A disposable-copy migration rule
- A structured evidence contract

Test the trigger:
- Positive: *"Add an order status column safely to workshop.db."* (Skill should activate)
- Negative: *"Explain what a SQLite index is."* (Skill should NOT activate)

### Phase 2: Add Progressive Disclosure (Stage C)
- Extract migration safety rules into `references/migration-rules.md`.
- Keep `SKILL.md` lean (<300 words) and direct the agent to read the checklist only when needed.

### Phase 3: Add Deterministic SQLite Evidence (Stage D)
- Create `scripts/sqlite_guard.py` with `inspect`, `query`, and `validate` commands.
- Open diagnostic queries in SQLite read-only mode.
- Validate migrations against a temporary copy and run integrity checks.

### Phase 4: Test Real Queries and Migrations (Stage E)
Try the prompts in `exercises/requests.md`, then select each migration:

```sh
python scripts/select_scenario.py 1  # Safe additive column and index
python scripts/select_scenario.py 2  # Required column without a backfill
python scripts/select_scenario.py 3  # Populated column deletion
python scripts/select_scenario.py reset
```

Ask the agent to validate `migrations/current.sql` against `workshop.db` without modifying the original.

## Fast-Forward Checkpoints

If you fall behind or want to inspect reference states:

```sh
python scripts/restore_checkpoint.py starter
python scripts/restore_checkpoint.py basic-skill
python scripts/restore_checkpoint.py complete-skill
```
