# SQL AI Database Solutions: Code and Real-World Examples

This repository is an academic example project that demonstrates how artificial intelligence can help users talk to databases using natural language and generate SQL queries. The demo uses Python, Streamlit, and SQLite to convert plain English questions into safe `SELECT` statements, execute them against a sample database, and display the results.

The project is designed for the assignment topic: **"SQL AI Database Solutions: Code and Real-World Examples"**.

## Features

- Streamlit web interface for natural language database questions.
- SQLite sample database with realistic business, student, sales, inventory, and customer support data.
- Schema extraction so the app can describe available tables and columns.
- Rule-based Text-to-SQL fallback that works without an API key.
- Optional Hugging Face integration through environment variables.
- SQL validation that allows `SELECT` queries only.
- Query execution and result display in a table.
- Tests for database setup, schema reading, SQL validation, and query execution.
- Academic article, video script, and partner comments document.

## Technologies Used

- Python 3.10+
- Streamlit
- SQLite
- Pandas
- Pytest
- Optional Hugging Face Inference API

## Repository Structure

```text
sql-ai-database-solutions/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── app.py
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── schema_reader.py
│   ├── query_generator.py
│   └── query_executor.py
├── data/
│   ├── sample.db
│   └── seed_data.sql
├── tests/
│   ├── test_database.py
│   └── test_query_executor.py
└── docs/
    ├── article.md
    ├── video-script.md
    └── partner-comments.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/sql-ai-database-solutions.git
cd sql-ai-database-solutions
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Streamlit App

```bash
streamlit run app.py
```

The app will create `data/sample.db` automatically from `data/seed_data.sql` if the database file is missing.

## Optional Hugging Face Setup

The demo works locally with a rule-based fallback. To try a Hugging Face Text-to-SQL model, set these environment variables before running the app:

```bash
set HF_API_TOKEN=your_token_here
set HF_MODEL=defog/sqlcoder-7b-2
```

On macOS or Linux:

```bash
export HF_API_TOKEN=your_token_here
export HF_MODEL=defog/sqlcoder-7b-2
```

If the Hugging Face request fails or returns unsafe SQL, the application falls back to the local generator.

## Run Tests

```bash
pytest
```

## Example Natural Language Questions

Try these questions in the Streamlit app:

- What are the top selling products by revenue?
- Which products are low in stock?
- Show total sales by month.
- List open high priority support tickets.
- Find active students in Computer Science.
- What is the average GPA by academic program?
- Show the best customers by total purchases.

## Public Repository Note

This repository is intended to be published as the public example repository for the academic assignment. Before publishing, replace `your-username` in the clone URL with the real GitHub or GitLab account name.

## Security Notes

This project intentionally uses SQLite and sample data for safety and simplicity. The generated SQL is limited to `SELECT` statements, and dangerous commands such as `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, and `TRUNCATE` are blocked.

Production systems require stronger protections, including database permissions, query allowlists, audit logs, rate limits, parameterized access patterns, human review for sensitive data, and careful monitoring.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
