from __future__ import annotations

import argparse

from scrape_pipeline import clean_records, create_database, discover_categories, scrape_category
from sql_queries import run_queries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--categories",
        type=int,
        default=3,
        help="Number of categories to scrape. Minimum is 3.",
    )
    args = parser.parse_args()

    if args.categories < 3:
        raise SystemExit("--categories must be at least 3.")

    categories = discover_categories()[: args.categories]
    print("Selected categories:", [c.name for c in categories])

    raw_records = []
    for category in categories:
        print(f"Scraping: {category.name}")
        raw_records.extend(scrape_category(category))

    df = clean_records(raw_records)
    print(f"Clean rows: {len(df)}")
    print(f"Categories: {df['category'].nunique()}")

    if len(df) < 60:
        raise RuntimeError("Acceptance criterion failed: fewer than 60 books.")
    if df["category"].nunique() < 3:
        raise RuntimeError("Acceptance criterion failed: fewer than 3 categories.")

    create_database(df)
    run_queries()

    print("SQLite database:", "data_pipeline/database/zepto_books.db")
    print("SQL log:", "data_pipeline/outputs/sql_outputs.md")
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
