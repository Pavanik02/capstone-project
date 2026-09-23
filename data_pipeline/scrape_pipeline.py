"""
Books to Scrape acquisition and cleaning pipeline.

The source is intentionally a public scraping-practice website. No API key is
required. The code is defensive around pagination, parsing and HTTP failures.
"""
from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
GBP_TO_INR = 105.50
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "database" / "zepto_books.db"
OUTPUT_DIR = ROOT / "outputs"

HEADERS = {
    "User-Agent": "Zepto-AI-ML-Capstone/1.0 (educational scraping exercise)"
}


@dataclass(frozen=True)
class Category:
    name: str
    url: str


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def discover_categories() -> list[Category]:
    soup = get_soup(BASE_URL)
    result: list[Category] = []
    for link in soup.select("div.side_categories ul li ul li a"):
        name = link.get_text(" ", strip=True)
        href = link.get("href")
        if href:
            result.append(Category(name=name, url=requests.compat.urljoin(BASE_URL, href)))
    if not result:
        raise RuntimeError("No categories were discovered from books.toscrape.com")
    return result


def parse_rating(card: BeautifulSoup) -> int | None:
    rating_tag = card.select_one("p.star-rating")
    if not rating_tag:
        return None
    classes = rating_tag.get("class", [])
    text = next((c for c in classes if c in RATING_MAP), None)
    return RATING_MAP.get(text) if text else None


def parse_price(text: str) -> float | None:
    cleaned = re.sub(r"[^0-9.]", "", text)
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_stock(text: str) -> bool:
    return "in stock" in text.lower()


def scrape_category(category: Category) -> list[dict]:
    records: list[dict] = []
    next_url: str | None = category.url

    while next_url:
        soup = get_soup(next_url)
        for card in soup.select("article.product_pod"):
            title_tag = card.select_one("h3 a")
            price_tag = card.select_one(".price_color")
            availability_tag = card.select_one(".availability")

            if not title_tag:
                continue

            records.append(
                {
                    "title": title_tag.get("title") or title_tag.get_text(" ", strip=True),
                    "price_raw": price_tag.get_text(" ", strip=True) if price_tag else "",
                    "rating_raw": " ".join(card.select_one("p.star-rating").get("class", []))
                    if card.select_one("p.star-rating") else "",
                    "availability_raw": availability_tag.get_text(" ", strip=True)
                    if availability_tag else "",
                    "category": category.name,
                }
            )

        next_link = soup.select_one("li.next a")
        next_url = requests.compat.urljoin(next_url, next_link["href"]) if next_link else None

    return records


def clean_records(records: Iterable[dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError("Scraping returned no rows.")

    df["price_gbp"] = df["price_raw"].map(parse_price)
    df["rating"] = df["rating_raw"].str.extract(
        r"\b(One|Two|Three|Four|Five)\b", expand=False
    ).map(RATING_MAP)
    df["in_stock"] = df["availability_raw"].map(parse_stock)

    # Rows without a stable catalog identity are dropped.
    df = df.dropna(subset=["title", "category"]).copy()

    # Numeric parsing failures are median-imputed as required by the task.
    for col in ["price_gbp", "rating"]:
        median = df[col].median()
        df[col] = df[col].fillna(median)

    df["rating"] = df["rating"].round().clip(1, 5).astype(int)
    df["price_gbp"] = df["price_gbp"].astype(float)
    df["price_inr"] = df["price_gbp"] * GBP_TO_INR
    df["in_stock"] = df["in_stock"].astype(bool)

    return df[
        ["title", "price_gbp", "price_inr", "rating", "in_stock", "category"]
    ].reset_index(drop=True)


def create_database(df: pd.DataFrame, db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        conn.executescript(
            """
            CREATE TABLE categories (
                category_id INTEGER PRIMARY KEY,
                category_name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE books (
                book_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                price_gbp REAL NOT NULL,
                price_inr REAL NOT NULL,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                in_stock INTEGER NOT NULL CHECK (in_stock IN (0, 1)),
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            );
            """
        )

        categories = sorted(df["category"].unique())
        conn.executemany(
            "INSERT INTO categories(category_name) VALUES (?)",
            [(c,) for c in categories],
        )

        category_map = dict(
            conn.execute("SELECT category_name, category_id FROM categories").fetchall()
        )

        rows = [
            (
                i,
                row.title,
                float(row.price_gbp),
                float(row.price_inr),
                int(row.rating),
                int(row.in_stock),
                category_map[row.category],
            )
            for i, row in enumerate(df.itertuples(index=False), start=1)
        ]

        conn.executemany(
            """
            INSERT INTO books
            (book_id, title, price_gbp, price_inr, rating, in_stock, category_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        conn.commit()
