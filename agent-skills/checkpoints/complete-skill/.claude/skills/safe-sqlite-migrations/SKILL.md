---
name: safe-sqlite-migrations
description: Inspects local SQLite databases, answers read-only data questions, and reviews or validates schema migrations without modifying the original database.
---

# Safe SQLite Migrations

Use this skill for SQLite schema changes, migration review, and targeted local data questions.

## Procedure

1. Confirm the database and migration paths; do not guess when multiple candidates exist.
2. Run `scripts/sqlite_guard.py inspect <database>` to collect schema and row-count evidence.
3. For data questions, use `scripts/sqlite_guard.py query <database> --sql "<SELECT...>"`. Keep queries read-only and show the SQL with the result.
4. Before reviewing or writing migration SQL, read `references/migration-rules.md`.
5. Run `scripts/sqlite_guard.py validate <database> <migration.sql>`. It applies SQL only to a temporary copy.
6. Report preconditions, validation output, data-loss warnings, postconditions, and rollback implications.

Never apply migration SQL to the original database unless the user explicitly requests it and confirms the target. A successful temporary execution is not proof that a migration is operationally safe.

## Response contract

- **Outcome:** `SAFE`, `UNSAFE`, or `NEEDS REVIEW`
- **Evidence:** schema, row counts, query output, and exact helper command
- **Migration concerns:** locking, backfill, constraints, data loss, and rollback
- **Next action:** one concrete, verifiable step
