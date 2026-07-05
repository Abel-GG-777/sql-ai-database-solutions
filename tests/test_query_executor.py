import pytest

from src.database import ensure_database, get_connection
from src.query_executor import execute_select_query
from src.query_generator import SqlValidationError, generate_rule_based_sql, validate_sql


def test_query_executor_runs_select_query(tmp_path):
    db_path = tmp_path / "sample.db"
    ensure_database(db_path)

    with get_connection(db_path) as connection:
        rows = execute_select_query(
            connection,
            "SELECT name, stock_quantity FROM products ORDER BY name LIMIT 3",
        )

    assert len(rows) == 3
    assert {"name", "stock_quantity"} <= set(rows[0])


@pytest.mark.parametrize(
    "unsafe_sql",
    [
        "DROP TABLE products",
        "DELETE FROM sales",
        "UPDATE products SET stock_quantity = 0",
        "INSERT INTO customers VALUES (99, 'Test', 'test@example.com', 'NA', 'Test')",
        "SELECT * FROM products; DROP TABLE products",
    ],
)
def test_validate_sql_blocks_dangerous_statements(unsafe_sql):
    with pytest.raises(SqlValidationError):
        validate_sql(unsafe_sql)


def test_rule_based_generator_returns_low_stock_query(tmp_path):
    db_path = tmp_path / "sample.db"
    ensure_database(db_path)
    sql = generate_rule_based_sql("Which products are low in stock?")

    with get_connection(db_path) as connection:
        rows = execute_select_query(connection, sql)

    assert rows
    assert rows[0]["stock_quantity"] <= rows[0]["reorder_level"]
