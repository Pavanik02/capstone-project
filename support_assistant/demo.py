import os
os.environ.setdefault("MOCK_LLM", "1")

from support_assistant.graph import build_graph


def main():
    graph = build_graph()
    examples = [
        "What is the delivery fee below INR 149?",
        "What is the capital of France?",
    ]
    for query in examples:
        result = graph.invoke({"query": query})
        print(query)
        print(result["response"])
        print()


if __name__ == "__main__":
    main()
