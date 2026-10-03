---
name: safe-sqlite-migrations
description: Inspects local SQLite databases, answers read-only data questions, and reviews or validates schema migrations without modifying the original database.
---

# Safe SQLite Migrations

Use this skill for SQLite schema changes, migration review, and targeted queries against a local database.

## Procedure

1. Locate the database and migration file. Ask before guessing when either is ambiguous.
2. Inspect the current schema and relevant data before proposing SQL.
3. Run diagnostic queries in read-only mode.
4. Validate migration SQL against a disposable database copy, never the original.
5. Report the SQL, evidence, migration outcome, and rollback implications.

Never apply a migration to the original database unless the user explicitly asks and confirms the target.
