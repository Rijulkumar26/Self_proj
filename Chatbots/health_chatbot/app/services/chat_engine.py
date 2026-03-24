from app.services.retriever import retrieve_docs
from app.services.llm import generate_response


def get_answer(query):
    docs = retrieve_docs(query)
    answer = generate_response(query, docs)

    return {
        "answer": answer,
        "sources": [
            {
                "policy": doc["policy_name"],
                "section": doc["section"]
            }
            for doc in docs
        ]
    }