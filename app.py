from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import DEFAULT_DB_PATH, ensure_database, get_connection
from src.query_executor import execute_select_query
from src.query_generator import SqlValidationError, generate_sql, validate_sql
from src.schema_reader import extract_schema, format_schema_for_prompt


EXAMPLE_QUESTIONS = [
    "What are the top selling products by revenue?",
    "Which products are low in stock?",
    "Show total sales by month.",
    "List open high priority support tickets.",
    "Find active students in Computer Science.",
    "What is the average GPA by academic program?",
    "Show the best customers by total purchases.",
]


def main() -> None:
    st.set_page_config(
        page_title="SQL AI Database Solutions",
        page_icon=":material/database:",
        layout="wide",
    )

    ensure_database(DEFAULT_DB_PATH)

    st.title("SQL AI Database Solutions")
    st.caption("Natural language to SQL demo using Python, Streamlit, and SQLite.")

    with get_connection(DEFAULT_DB_PATH) as connection:
        schema = extract_schema(connection)
        schema_prompt = format_schema_for_prompt(schema)

        left, right = st.columns([0.62, 0.38], gap="large")

        with left:
            selected_example = st.selectbox("Example questions", EXAMPLE_QUESTIONS)
            question = st.text_area(
                "Ask a question about the sample database",
                value=selected_example,
                height=110,
                placeholder="Example: Which products are low in stock?",
            )

            if st.button("Generate and run SQL", type="primary"):
                try:
                    sql = generate_sql(question, schema_prompt)
                    safe_sql = validate_sql(sql)
                    rows = execute_select_query(connection, safe_sql)
                except SqlValidationError as error:
                    st.error(f"The generated SQL was rejected: {error}")
                except Exception as error:  # Streamlit should show a friendly error.
                    st.error(f"Query execution failed: {error}")
                else:
                    st.subheader("Generated SQL")
                    st.code(safe_sql, language="sql")

                    st.subheader("Results")
                    if rows:
                        st.dataframe(pd.DataFrame(rows), use_container_width=True)
                    else:
                        st.info("The query ran successfully but returned no rows.")

        with right:
            st.subheader("Available database schema")
            st.code(schema_prompt, language="text")
            st.info(
                "This academic demo only allows SELECT queries. Production systems "
                "need stronger validation, permissions, logging, and human review."
            )


if __name__ == "__main__":
    main()
