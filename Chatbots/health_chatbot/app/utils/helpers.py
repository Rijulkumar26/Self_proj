def format_sources(docs):
    return list(set([
        f"{doc['policy_name']} - {doc['section']}"
        for doc in docs
    ]))