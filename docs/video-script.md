# Video Presentation Script: SQL AI Database Solutions

Estimated duration: under 5 minutes.

## 0:00-0:30 Introduction

Hello everyone. In this presentation, I will introduce my project, **SQL AI Database Solutions: Code and Real-World Examples**. The purpose of this repository is to show how artificial intelligence can help users ask questions in natural language and convert those questions into SQL queries.

The project uses Python, Streamlit, and SQLite. It is designed as a simple academic demo that is easy to run locally.

## 0:30-1:15 Problem and Motivation

Databases store important information such as sales, customers, products, students, and support tickets. However, many users do not know SQL, so they depend on technical staff to extract information.

Text-to-SQL helps solve this problem. A user can write a question like, "Which products are low in stock?" and the system generates an SQL query that can retrieve the answer from the database.

## 1:15-2:10 Project Architecture

The application has five main parts.

First, the Streamlit interface receives the natural language question.

Second, the database module connects to a local SQLite database.

Third, the schema reader extracts the available tables and columns.

Fourth, the query generator creates an SQL query. It supports an optional Hugging Face model, but it also includes a rule-based fallback so the demo works without an API key.

Fifth, the query executor validates the SQL and runs it only if it is a safe `SELECT` query.

## 2:10-3:15 Demo Examples

In the app, I can ask: "What are the top selling products by revenue?" The app generates a query that joins the sales and products tables, groups by product, and orders by revenue.

I can also ask: "Which products are low in stock?" The app generates a query that compares stock quantity with the reorder level.

For student data, I can ask: "Find active students in Computer Science." The query filters the students table by program and enrollment status.

For customer support, I can ask: "List open high priority support tickets." The app returns urgent tickets that are not closed.

## 3:15-4:10 Security and Limitations

Security is very important in AI database systems. This demo only allows `SELECT` queries. It blocks dangerous commands such as `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, and `TRUNCATE`.

However, this is still a basic academic example. A production system would need stronger validation, read-only database users, access control, logging, rate limits, privacy protection, and human review.

AI-generated SQL can also be wrong. It can misunderstand the question or choose the wrong column. That is why the app shows the generated SQL before showing the result.

## 4:10-4:50 Conclusion

In conclusion, SQL AI Database Solutions can make databases easier to use by allowing people to ask questions in natural language. This project demonstrates the basic workflow: natural language input, schema extraction, SQL generation, validation, execution, and result display.

The repository includes the Streamlit app, sample SQLite database, source code, tests, article, and presentation materials. Thank you.
