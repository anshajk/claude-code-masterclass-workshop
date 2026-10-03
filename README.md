# Ergosphere Labs masterclass workshops

This repository contains the hands-on projects for two Ergosphere Labs
masterclasses:

| Masterclass | Workshop |
|---|---|
| [Claude Code](https://ergospherelabs.com/masterclasses/claude-code/) | Google Agent Development Kit project at the repository root |
| Agent Skills | SQLite queries and safe migration skill under [`agent-skills/`](agent-skills/) |

Each workshop is intentionally small, deterministic, and resettable.

## Claude Code workshop

The root project covers repository orientation, debugging, and feature
delivery with Google ADK.

## Prerequisites

- Python 3.10 or newer
- Git
- Claude Code
- A Google API key only when running the agent; tests do not require one

## Setup

```sh
git clone https://github.com/anshajk/claude-code-masterclass-workshop.git
cd claude-code-masterclass-workshop
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp workshop_agent/.env.example workshop_agent/.env
```

Add your Google API key to `workshop_agent/.env`. The file is ignored by Git;
never commit a real credential.

## Run

```sh
adk run workshop_agent
adk web --port 8000
pytest -q
```

ADK Web is for local development and demonstration, not production hosting.

## Workshop checkpoints

The project includes three resettable checkpoints:

| Checkpoint | Purpose |
|---|---|
| `starter` | Contains the deterministic lookup bug used in the debugging exercise |
| `bug-fixed` | Normalizes module lookup input and includes the regression test |
| `feature-complete` | Adds the module-risk tool, agent instruction, and focused tests |

Restore a checkpoint at any time:

```sh
python scripts/restore_checkpoint.py starter
python scripts/restore_checkpoint.py bug-fixed
python scripts/restore_checkpoint.py feature-complete
```

The reset script changes only:

- `workshop_agent/agent.py`
- `workshop_agent/tools.py`
- `tests/test_tools.py`

## Suggested exercise

1. Restore `starter`.
2. Ask Claude Code to orient itself in the repository without making changes.
3. Run the tests and investigate the failing lookup behavior.
4. Implement and verify the smallest correct fix.
5. Ask Claude Code to add a deterministic module-risk tool with focused tests.
6. Compare the result with the supplied checkpoints.

The dependencies are pinned so the workshop behavior remains predictable.

## Agent Skills workshop

The [`agent-skills/`](agent-skills/) track builds a
`safe-sqlite-migrations` skill that:

- inspects a seeded local SQLite database;
- answers targeted questions through a read-only connection;
- validates migration SQL against a temporary copy; and
- reports invalid constraints and populated data at risk.

Start the exercise with:

```sh
cd agent-skills
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/setup_database.py
python scripts/restore_checkpoint.py starter
```

See [`agent-skills/README.md`](agent-skills/README.md) for the complete
exercise and checkpoint flow.
