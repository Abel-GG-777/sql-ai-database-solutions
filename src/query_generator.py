from __future__ import annotations

import os
import re
from dataclasses import dataclass


class SqlValidationError(ValueError):
    """Raised when generated SQL is not safe for this demo."""


BLOCKED_SQL_KEYWORDS = {
    "ALTER",
    "ATTACH",
    "CREATE",
    "DELETE",
    "DETACH",
    "DROP",
    "INSERT",
    "PRAGMA",
    "REINDEX",
    "REPLACE",
    "TRUNCATE",
    "UPDATE",
    "VACUUM",
}


@dataclass(frozen=True)
class RuleBasedExample:
    keywords: tuple[str, ...]
    sql: str


RULE_BASED_EXAMPLES = [
    RuleBasedExample(
        ("top", "selling", "product", "revenue"),
        """
        SELECT
            p.name AS product,
            p.category,
            SUM(s.quantity) AS units_sold,
            ROUND(SUM(s.total_amount), 2) AS revenue
        FROM sales s
        JOIN products p ON p.product_id = s.product_id
        GROUP BY p.product_id, p.name, p.category
        ORDER BY revenue DESC
        LIMIT 10
        """,
    ),
    RuleBasedExample(
        ("total", "sales", "month"),
        """
        SELECT
            strftime('%Y-%m', sale_date) AS month,
            ROUND(SUM(total_amount), 2) AS revenue,
            SUM(quantity) AS units_sold
        FROM sales
        GROUP BY month
        ORDER BY month
        """,
    ),
    RuleBasedExample(
        ("low", "stock"),
        """
        SELECT
            sku,
            name,
            category,
            stock_quantity,
            reorder_level,
            supplier
        FROM products
        WHERE stock_quantity <= reorder_level
        ORDER BY stock_quantity ASC
        """,
    ),
    RuleBasedExample(
        ("inventory", "reorder"),
        """
        SELECT
            sku,
            name,
            category,
            stock_quantity,
            reorder_level
        FROM products
        WHERE stock_quantity <= reorder_level
        ORDER BY category, name
        """,
    ),
    RuleBasedExample(
        ("support", "open", "high"),
        """
        SELECT
            t.ticket_id,
            c.full_name AS customer,
            t.issue_type,
            t.priority,
            t.status,
            t.created_at
        FROM support_tickets t
        JOIN customers c ON c.customer_id = t.customer_id
        WHERE t.status <> 'Closed'
          AND t.priority = 'High'
        ORDER BY t.created_at DESC
        """,
    ),
    RuleBasedExample(
        ("student", "computer science"),
        """
        SELECT
            student_id,
            full_name,
            program,
            year_level,
            gpa,
            enrollment_status
        FROM students
        WHERE program = 'Computer Science'
          AND enrollment_status = 'Active'
        ORDER BY gpa DESC
        """,
    ),
    RuleBasedExample(
        ("average", "gpa", "program"),
        """
        SELECT
            program,
            ROUND(AVG(gpa), 2) AS average_gpa,
            COUNT(*) AS student_count
        FROM students
        GROUP BY program
        ORDER BY average_gpa DESC
        """,
    ),
    RuleBasedExample(
        ("best", "customers", "purchases"),
        """
        SELECT
            c.full_name,
            c.region,
            c.segment,
            ROUND(SUM(s.total_amount), 2) AS total_purchases
        FROM customers c
        JOIN sales s ON s.customer_id = c.customer_id
        GROUP BY c.customer_id, c.full_name, c.region, c.segment
        ORDER BY total_purchases DESC
        LIMIT 10
        """,
    ),
    RuleBasedExample(
        ("sales", "channel"),
        """
        SELECT
            sales_channel,
            COUNT(*) AS transaction_count,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM sales
        GROUP BY sales_channel
        ORDER BY revenue DESC
        """,
    ),
]


def generate_sql(question: str, schema_text: str) -> str:
    """Generate SQL using optional Hugging Face integration or a local fallback."""
    if os.getenv("HF_API_TOKEN"):
        try:
            return _generate_with_hugging_face(question, schema_text)
        except Exception:
            # The local fallback keeps the demo usable in classrooms without API access.
            return generate_rule_based_sql(question)

    return generate_rule_based_sql(question)


def generate_rule_based_sql(question: str) -> str:
    normalized_question = _normalize_text(question)

    for example in RULE_BASED_EXAMPLES:
        if all(keyword in normalized_question for keyword in example.keywords):
            return example.sql

    if "customer" in normalized_question:
        return """
        SELECT
            customer_id,
            full_name,
            email,
            region,
            segment
        FROM customers
        ORDER BY full_name
        LIMIT 25
        """

    if "student" in normalized_question:
        return """
        SELECT
            student_id,
            full_name,
            program,
            year_level,
            gpa,
            enrollment_status
        FROM students
        ORDER BY full_name
        LIMIT 25
        """

    if "product" in normalized_question or "inventory" in normalized_question:
        return """
        SELECT
            sku,
            name,
            category,
            unit_price,
            stock_quantity
        FROM products
        ORDER BY category, name
        LIMIT 25
        """

    if "ticket" in normalized_question or "support" in normalized_question:
        return """
        SELECT
            ticket_id,
            customer_id,
            issue_type,
            status,
            priority,
            created_at
        FROM support_tickets
        ORDER BY created_at DESC
        LIMIT 25
        """

    return """
    SELECT
        sale_id,
        customer_id,
        product_id,
        sale_date,
        quantity,
        total_amount,
        sales_channel
    FROM sales
    ORDER BY sale_date DESC
    LIMIT 25
    """


def validate_sql(sql: str) -> str:
    cleaned_sql = _clean_sql(sql)
    if not cleaned_sql:
        raise SqlValidationError("SQL query is empty.")

    if cleaned_sql.endswith(";"):
        cleaned_sql = cleaned_sql[:-1].strip()

    if ";" in cleaned_sql:
        raise SqlValidationError("Only one SQL statement is allowed.")

    if "--" in cleaned_sql or "/*" in cleaned_sql or "*/" in cleaned_sql:
        raise SqlValidationError("SQL comments are not allowed in generated queries.")

    first_token_match = re.match(r"^\s*([A-Za-z]+)", cleaned_sql)
    first_token = first_token_match.group(1).upper() if first_token_match else ""
    if first_token != "SELECT":
        raise SqlValidationError("Only SELECT queries are allowed.")

    upper_sql = cleaned_sql.upper()
    for keyword in BLOCKED_SQL_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            raise SqlValidationError(f"Dangerous SQL keyword blocked: {keyword}")

    return cleaned_sql


def _generate_with_hugging_face(question: str, schema_text: str) -> str:
    import requests

    model = os.getenv("HF_MODEL", "defog/sqlcoder-7b-2")
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    prompt = f"""
You are a Text-to-SQL assistant. Generate exactly one SQLite SELECT query.
Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, or CREATE.
Do not explain the answer.

Database schema:
{schema_text}

User question:
{question}

SQL:
"""
    response = requests.post(
        api_url,
        headers={"Authorization": f"Bearer {os.environ['HF_API_TOKEN']}"},
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 180,
                "return_full_text": False,
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    if isinstance(payload, list) and payload:
        generated_text = payload[0].get("generated_text", "")
    elif isinstance(payload, dict):
        generated_text = payload.get("generated_text", "")
    else:
        generated_text = ""

    return validate_sql(generated_text)


def _clean_sql(sql: str) -> str:
    text = sql.strip()
    fenced_match = re.search(r"```(?:sql)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced_match:
        text = fenced_match.group(1).strip()
    text = re.sub(r"^\s*SQL\s*:\s*", "", text, flags=re.IGNORECASE)
    return text.strip()


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()
