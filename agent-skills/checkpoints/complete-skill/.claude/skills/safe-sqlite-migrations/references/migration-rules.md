# SQLite migration rules

Read this reference before proposing or validating schema changes.

## Preconditions

- Confirm the exact database and migration paths.
- Inspect table definitions, indexes, foreign keys, and affected row counts.
- Identify nulls, duplicates, and values that would violate new constraints.
- Treat `DROP TABLE`, `DROP COLUMN`, table rebuilds, and destructive backfills as data-loss operations.

## Safe execution

- Validate against a byte-for-byte temporary copy.
- Enable foreign keys and finish with `PRAGMA foreign_key_check` and `PRAGMA integrity_check`.
- Prefer additive, backward-compatible changes.
- Separate schema expansion, data backfill, and constraint enforcement when existing rows are involved.
- Keep query work read-only. Never turn a diagnostic prompt into an implicit write.

## Postconditions

- Verify expected columns, constraints, and indexes.
- Compare affected row counts before and after the migration.
- Re-run representative reads used by the application.
- State whether rollback is executable or requires restoring a backup.

## Reporting

Passing SQL execution proves only syntactic and immediate integrity. Report populated columns removed, irreversible transforms, long table rewrites, and compatibility assumptions even when validation succeeds.
