# Personal Expense Agent Design

**Status:** Draft for review  
**Date:** 2026-10-03

## Goal and scope

Add a personal expense-tracking agent alongside the existing Google ADK workshop app in this repository. It should let one person enter expenses through chat, review records, and get accurate date-range and category summaries. This is a personal tool using real financial data, not a workshop exercise.

The first version deliberately excludes bank connections, CSV imports, multi-device sync, budgets, charts, and multi-currency conversion.

## Agreed requirements

- Separate ADK app and expense package; do not add finance tools to `workshop_agent` or its resettable checkpoints.
- One-computer use, with a local SQLite ledger ignored by Git.
- INR is the default currency.
- Capture amount, date, description/merchant, optional category, and optional notes.
- Support listing expenses and summaries by date range or category.
- Require an explicit confirmation step before saving a new entry or changing an existing one.
- Archive rather than permanently erase deleted entries.
- Use deterministic Python code for storage, money handling, date filtering, and aggregation; the LLM interprets conversational requests but must not invent ledger facts or totals.
- The user accepts that Gemini processes the expense messages and records needed for replies.
- Automated tests should use temporary databases and must not need Gemini credentials.

## Architecture

Create an independently discoverable ADK app directory, tentatively `expense_agent/`, with a root agent and its own modules. Keep persistent ledger code in a focused module that can be called directly by deterministic tools. Avoid modifying the workshop agent's behavior, tool catalog, and checkpoints.

The expense service opens a configurable SQLite database path. The default should point to a user-local data directory outside the repository. Allow tests to inject a temporary database path. Add ignore rules for any in-repository local database and its SQLite sidecar files as defense in depth; do not store user records in source files, checkpoints, fixtures, or committed samples.

Use SQLite transactions and parameterized statements. Store money as a non-negative integer number of paise, not floating point. Store an ISO-8601 calendar date and a timestamp for when the row was recorded. Every operation that reads or writes the ledger filters out archived rows unless an explicit archive view is added later.

## Data model

An expense row contains:

- `id`: locally generated stable identifier.
- `amount_paise`: positive integer; INR is the initial and only supported currency.
- `spent_on`: ISO-8601 date (`YYYY-MM-DD`). If the user omits the date, use the host computer's local date.
- `description`: required, human-readable merchant or purchase description.
- `category`: optional string; do not silently assign a category when uncertain.
- `notes`: optional string.
- `created_at`: timestamp recorded by the application.
- `updated_at`: timestamp updated when a confirmed edit is applied.
- `archived_at`: nullable timestamp; non-null means the row is archived, not permanently deleted.

Database constraints should reject non-positive amounts and missing dates/descriptions. The application validates input and formats amounts as INR (two decimal places) at display boundaries.

## Agent and tool flow

Tools own side effects and return structured status results. The model must not claim an operation succeeded unless the corresponding tool reports success.

1. **Capture a proposed expense.** When the user's message has an unambiguous amount and description, parse the details and defaults, then present a human-readable draft with date, INR amount, description, category, and notes. Ask for confirmation. Do not write the draft to SQLite. If important fields are ambiguous, ask a concise clarification first.
2. **Confirm a draft.** Keep pending drafts in the ADK session state rather than inserting tentative ledger rows. On a clear confirmation, call a deterministic create tool with the reviewed fields. On a correction, update the draft and show it again; on a rejection, discard it. A confirmation must not be inferred from an unrelated message. The tool validates the draft again before committing.
3. **List.** Query active expenses in code, with optional date-range and category filters, stable ordering, and bounded result sizes. Return the exact records and indicate if results were limited.
4. **Summarize.** Compute totals and category breakdowns in Python/SQL over active records, filtered by the requested date range. Return both machine-readable amounts and display-ready INR strings; do not ask the model to calculate from a long list.
5. **Edit or archive.** Require a specific expense identifier or a uniquely matched record. Present the proposed change or archive action and wait for a separate confirmation before updating `updated_at` or setting `archived_at`. If matching is ambiguous, ask the user to choose rather than changing a record.

Session drafts are not a financial source of truth. Only committed, non-archived SQLite rows count toward reports. Initial scope does not include unarchive or permanent deletion; both can be considered later.

## Privacy and operational safety

- Local SQLite limits where the primary ledger is stored; it does **not** keep records from Gemini. Both the incoming chat text and retrieved records used in responses are model inputs under the agreed design.
- Do not log API credentials or full expense prompts/records. Error output should identify the operation and safe error class without copying personal content.
- Keep the database in the user's local data directory with restrictive filesystem permissions where supported. Do not commit database files, backups, or real expense data.
- The database is not application-encrypted in this version. Rely on device-level disk encryption and secure user-account access; communicate that limitation clearly.
- Do not add network listeners or remote database access for the local ledger.
- A transaction should be committed atomically. If validation or SQL fails, return a clear tool error and leave the original ledger unchanged.
- Treat model-generated tool parameters as untrusted: validate amount, date, description, category, identifier, and confirmation state in the deterministic layer.

## Error handling

Tools return a consistent success/error shape. Expected errors include invalid or non-positive amount, malformed/ambiguous date, missing description, invalid date range, unknown or ambiguous expense, missing confirmed draft, and database I/O/constraint failure. The agent should explain validation errors and ask for corrected details; it must not fabricate a fallback record or summary. If a database write fails, do not report success.

## Testing

Use unit tests with a temporary SQLite file or in-memory database to cover:

- INR rupee-to-paise parsing and display, including fractional amounts and invalid precision/input.
- Required-field and date validation; default date supplied by an injectable clock or explicit application boundary.
- Create, list, filtered list, stable ordering, and empty-ledger behavior.
- Exact totals and category breakdowns without floating-point drift.
- Draft creation, confirmation, rejection, and correction with no write before confirmation.
- Confirmed edit/archive, ambiguous lookup, and ensuring archived entries are excluded from ordinary reports.
- Database constraints and atomic failure behavior.

Tests must not call Gemini. Agent-specific configuration and tool registration can be checked offline. Live chat verification is conditional: a previous Gemini request in this workspace returned `403 PERMISSION_DENIED` (“Your project has been denied access”), so a successful live smoke test requires the project/model access issue to be resolved first.

## Acceptance criteria

1. ADK discovers and runs the expense app separately from `workshop_agent`.
2. Expense records are persisted locally and ignored by Git; workshop app files and checkpoints remain unchanged.
3. A proposed expense cannot enter the ledger until a separate explicit confirmation is received and validated.
4. Amounts and reports are precise in INR, including fractional rupees.
5. Listings and summaries are filtered and calculated deterministically from active SQLite records.
6. Edit and archive actions require confirmation; an archived record does not contribute to normal reports.
7. Automated tests run without external model credentials and cover the data and confirmation rules.
8. User-facing documentation explains Gemini data processing, local storage, lack of application-level encryption, setup, and how to run the separate app.

## Open implementation detail

Select and document the exact default user-local database path for supported platforms during implementation. Keep it configurable and outside the repository; tests must always pass an isolated temporary path.
