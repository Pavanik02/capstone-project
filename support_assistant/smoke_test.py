"""
Run after `python ingest.py` to verify routing and response schema in mock mode.
"""
import os
os.environ.setdefault("MOCK_LLM", "1")

from .graph import build_graph
from .models import AnswerResponse


def main():
    graph = build_graph()

    policy = graph.invoke({"query": "How much is the delivery fee below INR 149?"})
    general = graph.invoke({"query": "What is the capital of France?"})

    policy_response = AnswerResponse.model_validate(policy["response"])
    general_response = AnswerResponse.model_validate(general["response"])

    assert policy["intent"] == "policy_question"
    assert general["intent"] == "general_question"
    assert policy_response.sources
    assert not general_response.sources
    assert policy_response.answer.startswith("Based on the retrieved context:")
    assert general_response.answer == "I can only answer questions about Zepto policies right now."

    print("Support assistant mock-mode smoke test passed.")


if __name__ == "__main__":
    main()
