.PHONY: install data-pipeline support-index support-api

install:
	python -m pip install -r requirements.txt

data-pipeline:
	python data_pipeline/run_pipeline.py

support-index:
	python support_assistant/ingest.py

support-api:
	MOCK_LLM=1 uvicorn support_assistant.main:app --host 0.0.0.0 --port 7860
