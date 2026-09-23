from __future__ import annotations

import json
import os
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from pydantic import ValidationError

from .models import AnswerResponse
from .prompts import CORRECTION_PROMPT, build_prompt
from .rag import LocalRAG, mock_enabled


POLICY_KEYWORDS = (
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours",
)


class GraphState(TypedDict, total=False):
    query: str
    intent: Literal["policy_question", "general_question"]
    retrieved: list[dict]
    response: dict


def classify_intent(state: GraphState) -> GraphState:
    query = state["query"]
    if mock_enabled():
        lower = query.lower()
        intent = (
            "policy_question"
            if any(keyword in lower for keyword in POLICY_KEYWORDS)
            else "general_question"
        )
        return {"intent": intent}

    # Optional real-LLM extension.
    from langchain_groq import ChatGroq

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        temperature=0,
        api_key=os.environ["GROQ_API_KEY"],
    )
    prompt = (
        "Classify the user query as exactly one of policy_question or "
        "general_question. Output only the label.\n\nQuery: " + query
    )
    raw = model.invoke(prompt).content.strip().lower()
    intent = "policy_question" if "policy_question" in raw else "general_question"
    return {"intent": intent}


def retrieve_and_answer(state: GraphState) -> GraphState:
    rag = LocalRAG()
    retrieved = rag.retrieve(state["query"], k=3)
    if not retrieved:
        response = AnswerResponse(
            answer="The policy corpus did not return relevant context.",
            sources=[],
            confidence=0.0,
        )
        return {"retrieved": [], "response": response.model_dump()}

    if mock_enabled():
        top = retrieved[0]
        snippet = top["document"][:200].strip()
        response = AnswerResponse(
            answer=f"Based on the retrieved context: {snippet}",
            sources=[item["id"] for item in retrieved],
            confidence=1.0,
        )
        return {"retrieved": retrieved, "response": response.model_dump()}

    # Optional real-LLM extension with structured-output retry.
    from langchain_groq import ChatGroq

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        temperature=0,
        api_key=os.environ["GROQ_API_KEY"],
    )
    context = "\n\n".join(
        f"[{item['id']}]\n{item['document']}" for item in retrieved
    )
    prompt = build_prompt(state["query"], context)
    last_error = None

    for attempt in range(3):
        try:
            raw = model.invoke(prompt).content
            parsed = json.loads(raw)
            response = AnswerResponse.model_validate(parsed)
            return {"retrieved": retrieved, "response": response.model_dump()}
        except (json.JSONDecodeError, ValidationError, TypeError) as exc:
            last_error = exc
            prompt = (
                prompt
                + "\n\n"
                + CORRECTION_PROMPT
                + f"\nAttempt {attempt + 1} failed; correct the output."
            )

    error_response = AnswerResponse(
        answer=f"ERROR: structured output validation failed: {last_error}",
        sources=[item["id"] for item in retrieved],
        confidence=0.0,
    )
    return {"retrieved": retrieved, "response": error_response.model_dump()}


def direct_answer(state: GraphState) -> GraphState:
    if mock_enabled():
        response = AnswerResponse(
            answer="I can only answer questions about Zepto policies right now.",
            sources=[],
            confidence=1.0,
        )
        return {"response": response.model_dump()}

    from langchain_groq import ChatGroq

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        temperature=0,
        api_key=os.environ["GROQ_API_KEY"],
    )
    prompt = (
        "Answer the user directly. Return JSON with answer, sources and "
        "confidence. Sources must be an empty list because no retrieval was used.\n"
        f"User query: {state['query']}"
    )

    last_error = None
    for attempt in range(3):
        try:
            parsed = json.loads(model.invoke(prompt).content)
            parsed["sources"] = []
            return {"response": AnswerResponse.model_validate(parsed).model_dump()}
        except (json.JSONDecodeError, ValidationError, TypeError) as exc:
            last_error = exc
            prompt += "\nReturn only valid JSON matching the required schema."

    return {
        "response": AnswerResponse(
            answer=f"ERROR: structured output validation failed: {last_error}",
            sources=[],
            confidence=0.0,
        ).model_dump()
    }


def route(state: GraphState) -> str:
    return state["intent"]


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve_and_answer", retrieve_and_answer)
    graph.add_node("direct_answer", direct_answer)

    graph.add_edge(START, "classify_intent")
    graph.add_conditional_edges(
        "classify_intent",
        route,
        {
            "policy_question": "retrieve_and_answer",
            "general_question": "direct_answer",
        },
    )
    graph.add_edge("retrieve_and_answer", END)
    graph.add_edge("direct_answer", END)
    return graph.compile()
