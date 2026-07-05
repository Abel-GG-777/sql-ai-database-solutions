from src.database import ensure_database, get_connection
from src.schema_reader import extract_schema, format_schema_for_prompt


def test_ensure_database_creates_sample_database(tmp_path):
    db_path = tmp_path / "sample.db"

    ensure_database(db_path)

    assert db_path.exists()
    with get_connection(db_path) as connection:
        table_count = connection.execute(
            "SELECT COUNT(*) AS count FROM sqlite_master WHERE type = 'table'"
        ).fetchone()["count"]

    assert table_count >= 7


def test_schema_extraction_includes_expected_tables(tmp_path):
    db_path = tmp_path / "sample.db"
    ensure_database(db_path)

    with get_connection(db_path) as connection:
        schema = extract_schema(connection)
        schema_text = format_schema_for_prompt(schema)

    assert "customers" in schema
    assert "products" in schema
    assert "sales" in schema
    assert "support_tickets" in schema_text
