from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "database" / "zepto_books.db"
OUTPUT_PATH = ROOT / "outputs" / "sql_outputs.md"

QUERIES = {
    "01_select_where": """
        SELECT title, price_gbp, rating
        FROM books
        WHERE rating >= 4
        ORDER BY rating DESC, price_gbp DESC
        LIMIT 10;
    """,
    "02_order_by_limit": """
        SELECT title, price_gbp
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10;
    """,
    "03_distinct_categories": """
        SELECT DISTINCT category_name
        FROM categories
        ORDER BY category_name;
    """,
    "04_between_prices": """
        SELECT title, price_gbp, price_inr
        FROM books
        WHERE price_gbp BETWEEN 10 AND 30
        ORDER BY price_gbp;
    """,
    "05_in_ratings": """
        SELECT title, rating, in_stock
        FROM books
        WHERE rating IN (4, 5)
        ORDER BY rating DESC, title
        LIMIT 15;
    """,
    "06_join_category": """
        SELECT c.category_name, b.title, b.rating, b.price_gbp, b.in_stock
        FROM books AS b
        JOIN categories AS c
          ON b.category_id = c.category_id
        WHERE b.rating >= 4
        ORDER BY c.category_name, b.rating DESC, b.title
        LIMIT 20;
    """,
    "07_stock_filter": """
        SELECT title, price_gbp, in_stock
        FROM books
        WHERE in_stock = 1
        ORDER BY price_gbp ASC
        LIMIT 15;
    """,
    "08_category_counts": """
        SELECT c.category_name, COUNT(*) AS book_count
        FROM categories AS c
        JOIN books AS b ON b.category_id = c.category_id
        GROUP BY c.category_id, c.category_name
        ORDER BY book_count DESC, c.category_name;
    """,
}


def run_queries() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sections = ["# SQL Query Log", ""]
    with sqlite3.connect(DB_PATH) as conn:
        for name, query in QUERIES.items():
            result = pd.read_sql_query(query, conn)
            sections += [
                f"## {name}",
                "```sql",
                query.strip(),
                "```",
                "",
                result.to_markdown(index=False),
                "",
            ]

        join_sql = QUERIES["06_join_category"]
        sql_df = pd.read_sql_query(join_sql, conn)

        books_df = pd.read_sql_query(
            """
            SELECT book_id, title, price_gbp, price_inr, rating, in_stock, category_id
            FROM books
            """,
            conn,
        )
        categories_df = pd.read_sql_query(
            "SELECT category_id, category_name FROM categories", conn
        )

    merge_df = (
        books_df.merge(categories_df, on="category_id", how="inner")
        .loc[lambda x: x["rating"] >= 4,
             ["category_name", "title", "rating", "price_gbp", "in_stock"]]
        .sort_values(["category_name", "rating", "title"], ascending=[True, False, True])
        .head(20)
        .reset_index(drop=True)
    )

    sql_norm = sql_df.reset_index(drop=True).copy()
    merge_norm = merge_df.reset_index(drop=True).copy()
    sql_norm["in_stock"] = sql_norm["in_stock"].astype(bool)
    merge_norm["in_stock"] = merge_norm["in_stock"].astype(bool)
    equivalent = sql_norm.equals(merge_norm)

    sections += [
        "## SQL JOIN vs pandas merge",
        "",
        "### `pd.read_sql` result",
        sql_norm.to_markdown(index=False),
        "",
        "### `pd.merge` result",
        merge_norm.to_markdown(index=False),
        "",
        f"**Equivalent after column/type normalization:** `{equivalent}`",
        "",
    ]

    OUTPUT_PATH.write_text("\n".join(sections))


if __name__ == "__main__":
    run_queries()
