# Workshop requests

Use these prompts after restoring the desired skill checkpoint.

## Read-only queries

1. "Which active customers have never placed an order? Use the local SQLite database."
2. "Find orders whose stored total does not match the sum of their line items."

## Migration review

Select a migration with `python scripts/select_scenario.py <1|2|3>`, then ask:

> Validate `migrations/current.sql` against `workshop.db`. Do not modify the original database.

Expected outcomes:

- Scenario 1 applies cleanly and preserves integrity.
- Scenario 2 fails because existing rows cannot satisfy the required column.
- Scenario 3 applies on the disposable copy but is unsafe because populated data would be removed.
