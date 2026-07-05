from __future__ import annotations

import sqlite3
from typing import Any


def list_tables(connection: sqlite3.Connection) -> list[str]:
    query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """
    return [row["name"] for row in connection.execute(query).fetchall()]


def get_table_columns(connection: sqlite3.Connection, table_name: str) -> list[dict[str, Any]]:
    safe_table_name = table_name.replace('"', '""')
    rows = connection.execute(f'PRAGMA table_info("{safe_table_name}")').fetchall()
    return [
        {
            "name": row["name"],
            "type": row["type"],
            "required": bool(row["notnull"]),
            "primary_key": bool(row["pk"]),
        }
        for row in rows
    ]


def extract_schema(connection: sqlite3.Connection) -> dict[str, list[dict[str, Any]]]:
    return {table: get_table_columns(connection, table) for table in list_tables(connection)}


def format_schema_for_prompt(schema: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = []
    for table_name, columns in schema.items():
        column_parts = [f"{column['name']} {column['type']}" for column in columns]
        lines.append(f"{table_name}({', '.join(column_parts)})")
    return "\n".join(lines)


def format_schema_as_markdown(schema: dict[str, list[dict[str, Any]]]) -> str:
    sections: list[str] = []
    for table_name, columns in schema.items():
        sections.append(f"### {table_name}")
        sections.append("| Column | Type | Required | Primary key |")
        sections.append("| --- | --- | --- | --- |")
        for column in columns:
            sections.append(
                f"| {column['name']} | {column['type']} | "
                f"{'Yes' if column['required'] else 'No'} | "
                f"{'Yes' if column['primary_key'] else 'No'} |"
            )
        sections.append("")
    return "\n".join(sections)
