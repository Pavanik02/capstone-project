# Zepto Data & AI Platform

An end-to-end AI/ML engineering capstone containing three connected capabilities:

1. **`data_pipeline/`** — scrape, clean, enrich and normalize catalog-style data into SQLite, then query it with SQL and pandas.
2. **`analytics/`** — profile and clean the Titanic dataset, perform EDA, build/evaluate classifiers, compare imbalance strategies, tune a Random Forest, and solve a fare-regression side task.
3. **`support_assistant/`** — build a local RAG support service over eight Zepto policy documents using Sentence Transformers, ChromaDB, LangGraph and FastAPI.

All modules are in one repository. The project uses **one consolidated `requirements.txt` at the repository root**.

## 1. Setup

Python 3.10+ is recommended.

```bash
git clone <YOUR_PUBLIC_REPOSITORY_URL>
cd zepto-data-ai-platform

python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
```

The required baseline does not need a paid service or an LLM API key.

## 2. Module 1 — data pipeline

The scraper uses `requests` and `BeautifulSoup` against `https://books.toscrape.com/`. It collects all books from at least three categories, following pagination until each selected category is exhausted.

The required conversion is deliberately fixed and does not use an external currency service:

> **1 GBP = 105.50 INR**

Run:

```bash
python data_pipeline/run_pipeline.py
```

This performs:

1. category discovery;
2. scraping;
3. cleaning and type conversion;
4. GBP→INR enrichment;
5. normalized SQLite creation;
6. required SQL queries;
7. pandas `read_sql` checks;
8. SQL-vs-`merge` equivalence check.

The SQLite database is intentionally regenerated rather than treated as a source-of-truth binary artifact. This keeps the repository reproducible from the source script.

More detail: `data_pipeline/README.md`.

## 3. Module 2 — analytics

The first notebook is the **only place that loads the raw Titanic dataset** through Seaborn:

```python
sns.load_dataset("titanic")
```

Immediately after loading, it writes `analytics/titanic.csv`. If the online loader is unavailable, the notebook uses this committed CSV as the offline grading fallback.

Run:

```bash
jupyter notebook analytics/01_eda.ipynb
```

Run all cells. Then:

```bash
jupyter notebook analytics/02_modeling.ipynb
```

The second notebook reads the same committed `titanic.csv`; it never calls `sns.load_dataset("titanic")`.

The modeling pipeline uses train-only preprocessing through a scikit-learn `ColumnTransformer` and `Pipeline`. SMOTE is applied only to training data. The final fitted pipeline is saved as:

```text
analytics/artifacts/best_pipeline.joblib
```

More detail: `analytics/README.md`.

## 4. Module 3 — support assistant

The required baseline is completely local:

- Sentence Transformers: `all-MiniLM-L6-v2`
- ChromaDB
- LangGraph
- FastAPI
- deterministic mock generation

No LLM API key is required.

First build the local vector store:

```bash
python support_assistant/ingest.py
```

Then start the API:

```bash
MOCK_LLM=1 uvicorn support_assistant.main:app --host 0.0.0.0 --port 7860
```

Example policy request:

```bash
curl -X POST http://127.0.0.1:7860/ask   -H "Content-Type: application/json"   -d '{"query":"How much is the delivery fee for an order below INR 149?"}'
```

Example general request:

```bash
curl -X POST http://127.0.0.1:7860/ask   -H "Content-Type: application/json"   -d '{"query":"What is the capital of France?"}'
```

`MOCK_LLM` is unset or `1` by default. In this mode:

- intent classification uses the required keyword heuristic;
- retrieval still uses real embeddings + ChromaDB;
- answer generation is deterministic;
- no LLM network call is made.

The optional `MOCK_LLM=0` path is implemented for a Groq backend. It is not required for grading.

### Docker

From the repository root:

```bash
docker build -t zepto-support ./support_assistant
docker run --rm -p 7860:7860 -e MOCK_LLM=1 zepto-support
```

Then call `/ask` as above.

More detail: `support_assistant/README.md`.

## 5. Design decisions

### Data pipeline

The scraper separates acquisition from normalization. Raw text is parsed defensively: malformed numeric ratings/prices are handled with median imputation where a numeric value is required, while a row with an unusable identity/category is dropped because retaining an unidentifiable relational record would be less useful than losing that record. Categories are normalized into a separate table so category names are not duplicated in every book row. SQLite foreign keys are explicitly enabled.

### Analytics

EDA and modeling are intentionally separated into two ordered notebooks but share the same cleaned/offline dataset. The exploratory standardization step is a sanity check only; the modeling pipeline has its own train-only scaler. A `ColumnTransformer` prevents accidental fitting of preprocessing steps on the test set. SMOTE is restricted to training data. Model metrics are reported without collapsing classification and regression metrics onto one artificial scale.

### Support assistant

The corpus is treated as the authoritative knowledge base. Documents are chunked at one chunk per policy document because the supplied documents are short. ChromaDB performs cosine-similarity retrieval. LangGraph owns routing, while Pydantic owns the final response contract. The mock branch is deterministic and therefore suitable for grading without credentials or external model calls.

## 6. Git workflow

The submission should show a feature branch with at least two commits and a merge back into `main`. A reproducible sequence is:

```bash
git checkout -b feature/capstone-platform
git add .
git commit -m "Add data pipeline and analytics modules"

git add .
git commit -m "Add grounded support assistant"

git checkout main
git merge --no-ff feature/capstone-platform -m "Merge capstone platform feature"
```

Verify:

```bash
git log --graph --oneline --decorate --all
```

## 7. Submission

Submit exactly **one public GitHub repository URL** for this repository. Do not create separate repositories for the three modules.
