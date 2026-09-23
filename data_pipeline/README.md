# Data Pipeline

## Scope

This module scrapes catalog data from Books to Scrape, cleans the fields, converts GBP prices using the required fixed project rate, stores the result in normalized SQLite tables, and demonstrates SQL/pandas querying.

## Run

From repository root:

```bash
python data_pipeline/run_pipeline.py
```

Optional:

```bash
python data_pipeline/run_pipeline.py --categories 3
```

The script discovers categories and uses the first N categories when no explicit category list is supplied. It continues pagination until each chosen category is exhausted and asserts that at least 60 books were collected.

## Cleaning decisions

- `price_gbp`: currency symbol and surrounding whitespace are removed, then parsed as `float`.
- `rating`: the text values One–Five are mapped to integers 1–5.
- `in_stock`: the availability string is normalized to a boolean based on whether it contains `in stock`.
- Unexpected numeric values are median-imputed after valid rows have been parsed.
- A row missing a usable title or category is dropped because those fields are needed for a meaningful catalog/relational identity.
- `price_inr` is always calculated as `price_gbp * 105.50`.
- The conversion is a fixed assignment constant, not a live exchange rate.

## Relational design

`categories(category_id, category_name)` stores each category once.

`books(book_id, title, price_gbp, price_inr, rating, in_stock, category_id)` stores book facts and references `categories.category_id`.

SQLite foreign-key enforcement is enabled.

## SQL coverage

The pipeline executes more than the five minimum queries. The query set collectively demonstrates:

- `SELECT`
- `WHERE`
- `ORDER BY`
- `LIMIT`
- `DISTINCT`
- `IN`
- `BETWEEN`
- `JOIN`

Query strings and outputs are written to `data_pipeline/outputs/sql_outputs.md` on each run.

The pipeline also reads at least two SQL results using `pd.read_sql()` and independently reproduces the join using `pd.merge()`. It writes an equivalence assertion to the run output.
