#!/usr/bin/env python3
"""Read-only SQLite inspection and disposable-copy migration validation."""

import argparse
import re
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
DROP_COLUMN = re.compile(
    r"\bALTER\s+TABLE\s+([A-Za-z_][A-Za-z0-9_]*)\s+DROP\s+COLUMN\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.IGNORECASE,
)
DROP_TABLE = re.compile(
    r"\bDROP\s+TABLE(?:\s+IF\s+EXISTS)?\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.IGNORECASE,
)


def readonly_connection(database: Path) -> sqlite3.Connection:
    if not database.is_file():
        raise FileNotFoundError(f"Database not found: {database}")
    connection = sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True)
    connection.execute("PRAGMA query_only = ON")
    connection.row_factory = sqlite3.Row
    return connection


def quote_identifier(identifier: str) -> str:
    if not IDENTIFIER.fullmatch(identifier):
        raise ValueError(f"Unsafe SQLite identifier: {identifier!r}")
    return f'"{identifier}"'


def user_tables(connection: sqlite3.Connection) -> list[str]:
    rows = connection.execute(
        "SELECT name FROM sqlite_schema "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    return [row[0] for row in rows]


def inspect_database(database: Path) -> None:
    with readonly_connection(database) as connection:
        for table in user_tables(connection):
            count = connection.execute(
                f"SELECT COUNT(*) FROM {quote_identifier(table)}"
            ).fetchone()[0]
            schema = connection.execute(
                "SELECT sql FROM sqlite_schema WHERE type = 'table' AND name = ?",
                (table,),
            ).fetchone()[0]
            print(f"=== {table} ({count} rows) ===")
            print(schema)


def run_query(database: Path, sql: str) -> None:
    with readonly_connection(database) as connection:
        cursor = connection.execute(sql)
        if cursor.description is None:
            raise ValueError("Query produced no result set; only read-only queries are allowed.")
        columns = [column[0] for column in cursor.description]
        print("\t".join(columns))
        for row in cursor:
            print("\t".join("NULL" if value is None else str(value) for value in row))


def destructive_warnings(connection: sqlite3.Connection, migration_sql: str) -> list[str]:
    warnings = []
    for table, column in DROP_COLUMN.findall(migration_sql):
        count = connection.execute(
            f"SELECT COUNT(*) FROM {quote_identifier(table)} "
            f"WHERE {quote_identifier(column)} IS NOT NULL"
        ).fetchone()[0]
        warnings.append(f"DROPS {table}.{column}, which has {count} non-null values")
    for table in DROP_TABLE.findall(migration_sql):
        count = connection.execute(
            f"SELECT COUNT(*) FROM {quote_identifier(table)}"
        ).fetchone()[0]
        warnings.append(f"DROPS table {table}, which has {count} rows")
    return warnings


def validate_migration(database: Path, migration: Path) -> int:
    if not database.is_file():
        raise FileNotFoundError(f"Database not found: {database}")
    if not migration.is_file():
        raise FileNotFoundError(f"Migration not found: {migration}")

    migration_sql = migration.read_text()
    with readonly_connection(database) as source:
        warnings = destructive_warnings(source, migration_sql)

    with tempfile.TemporaryDirectory(prefix="sqlite-migration-") as temp_dir:
        copy_path = Path(temp_dir) / database.name
        shutil.copy2(database, copy_path)
        try:
            with sqlite3.connect(copy_path) as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                connection.executescript(migration_sql)
                foreign_key_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
                integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
                if foreign_key_errors or integrity != "ok":
                    print(
                        f"UNSAFE: integrity={integrity}, foreign_key_errors={len(foreign_key_errors)}"
                    )
                    return 1
        except sqlite3.Error as error:
            print(f"UNSAFE: migration failed on temporary copy: {error}")
            return 1

    if warnings:
        print("NEEDS REVIEW: migration executed on the temporary copy.")
        for warning in warnings:
            print(f"WARNING: {warning}")
        return 2

    print("SAFE: migration executed on a temporary copy; integrity checks passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("database", type=Path)

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("database", type=Path)
    query_parser.add_argument("--sql", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("database", type=Path)
    validate_parser.add_argument("migration", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "inspect":
            inspect_database(args.database)
            return 0
        if args.command == "query":
            run_query(args.database, args.sql)
            return 0
        return validate_migration(args.database, args.migration)
    except (FileNotFoundError, ValueError, sqlite3.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
