# Support Assistant

## Baseline

The graded path is completely offline with respect to LLM calls. Leave `MOCK_LLM` unset or set it to `1`.

Embeddings use the local `all-MiniLM-L6-v2` Sentence Transformer. ChromaDB stores vectors locally. LangGraph routes the query. FastAPI exposes the `/ask` endpoint.

## Build the index

From repository root:

```bash
python support_assistant/ingest.py
```

This reads all eight files under `docs/`, creates one chunk per supplied policy document, embeds the chunks and stores them in the `zepto_policy` Chroma collection under `chroma_db/`.

## Run

```bash
MOCK_LLM=1 uvicorn support_assistant.main:app --host 0.0.0.0 --port 7860
```

The mock default is deterministic:

- `classify_intent` uses the required keyword list.
- `retrieve_and_answer` performs real Chroma similarity retrieval and returns the first ~200 characters of the top chunk.
- `direct_answer` returns a fixed policy-scope message.
- the Pydantic response is constructed directly by application code.

## Example calls

After starting the server:

```bash
curl -X POST http://127.0.0.1:7860/ask   -H "Content-Type: application/json"   -d '{"query":"What is the delivery fee below INR 149?"}'
```

Expected response shape:

```json
{
  "answer": "Based on the retrieved context: Delivery Policy: ...",
  "sources": ["doc_01_chunk_01"],
  "confidence": 1.0
}
```

And:

```bash
curl -X POST http://127.0.0.1:7860/ask   -H "Content-Type: application/json"   -d '{"query":"What is the capital of France?"}'
```

Expected response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

The exact retrieved excerpt depends on the embedding model and is therefore produced by the application rather than hard-coded in this README.

## Architecture

```text
INGESTION
docs/doc_01.txt ... docs/doc_08.txt
        |
        v
ingest.py -> one chunk/document + metadata
        |
        v
EMBEDDING
SentenceTransformer("all-MiniLM-L6-v2")
        |
        v
STORAGE
ChromaDB collection: "zepto_policy"
        |
        v
ROUTING
LangGraph classify_intent
       / policy/   \general
     /           v         v
retrieve_and_answer   direct_answer
    |
    v
RETRIEVAL
Chroma query(n_results=3, cosine similarity)
    |
    v
GENERATION
mock deterministic answer OR optional real LLM prompt
    |
    v
Pydantic AnswerResponse
    |
    v
FastAPI POST /ask
```

### Stage-by-stage data flow

**Ingestion:** `ingest.py` reads the eight exact corpus files and creates one chunk per file. Each chunk receives an ID such as `doc_01_chunk_01` and source metadata.

**Embedding:** `rag.py` loads `all-MiniLM-L6-v2` locally and turns each chunk into a vector.

**Storage:** `ingest.py` stores vectors, text and metadata in the persistent ChromaDB collection named `zepto_policy`.

**Retrieval:** `retrieve_and_answer` in `graph.py` embeds the query through the same embedding model and asks ChromaDB for the top three results using cosine similarity.

**Generation:** in mock mode, `retrieve_and_answer` uses the first retrieved chunk to form a deterministic grounded response. In the optional real-LLM mode, `prompts.py` supplies a structured role-context-task-format-length prompt and the real model generates the answer.

**Routing:** `classify_intent` always owns the policy/general decision. Its mock branch uses the required keyword heuristic; its optional real branch can ask the LLM to classify. Retrieval itself does not branch on `MOCK_LLM`.

**Validation:** `models.py` validates every final response against `answer`, `sources`, and bounded `confidence`. The optional real-LLM path retries invalid structured output up to two additional times with a corrective instruction.

## Structured prompt

The optional real-LLM prompt follows the requested skeleton:

- **Role:** You are Zepto's policy support assistant.
- **Context:** Only the retrieved policy chunks are authoritative.
- **Task:** Answer the user's question using those chunks.
- **Format:** Return JSON with `answer`, `sources`, and `confidence`.
- **Length:** Keep the answer concise.
- **Negative constraint:** Do not answer using information that is not present in the provided context.
- **Few-shot example:** an example policy question, context and valid JSON response are included in `prompts.py`.

## Docker

Build:

```bash
docker build -t zepto-support support_assistant
```

Run:

```bash
docker run --rm -p 7860:7860 -e MOCK_LLM=1 zepto-support
```

The image runs Uvicorn on port 7860.

## Optional real LLM

Set `MOCK_LLM=0` and configure:

```text
GROQ_API_KEY=...
GROQ_MODEL=llama-3.1-8b-instant
```

The key is never hard-coded. The real path is optional and is not needed for the required graded baseline.
