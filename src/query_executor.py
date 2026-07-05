from __future__ import annotations

import sqlite3
from typing import Any

from src.query_generator import validate_sql


def execute_select_query(connection: sqlite3.Connection, sql: str) -> list[dict[str, Any]]:
    """Validate and execute a safe SELECT query."""
    safe_sql = validate_sql(sql)
    cursor = connection.execute(safe_sql)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
