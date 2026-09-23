from pathlib import Path

ROOT = Path(__file__).resolve().parent
required = [
    "README.md",
    "requirements.txt",
    "data_pipeline/run_pipeline.py",
    "data_pipeline/scrape_pipeline.py",
    "data_pipeline/sql_queries.py",
    "analytics/01_eda.ipynb",
    "analytics/02_modeling.ipynb",
    "analytics/titanic.csv",
    "support_assistant/main.py",
    "support_assistant/graph.py",
    "support_assistant/rag.py",
    "support_assistant/ingest.py",
    "support_assistant/Dockerfile",
]
missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit("Missing: " + ", ".join(missing))
print("Repository structure check passed.")
