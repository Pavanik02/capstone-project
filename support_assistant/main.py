from fastapi import FastAPI

from .graph import build_graph
from .models import AnswerResponse, AskRequest

app = FastAPI(
    title="Zepto Policy Support Assistant",
    version="1.0.0",
)

graph = build_graph()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(request: AskRequest) -> AnswerResponse:
    result = graph.invoke({"query": request.query})
    return AnswerResponse.model_validate(result["response"])
