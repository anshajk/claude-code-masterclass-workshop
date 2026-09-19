# Claude Code masterclass workshop

This repository contains the hands-on Google Agent Development Kit (ADK)
project used in the
[Ergosphere Labs Claude Code masterclass](https://ergospherelabs.com/masterclasses/claude-code/).
It is intentionally small enough to understand during a live session and
includes deterministic exercises for repository orientation, debugging, and
feature delivery.

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
