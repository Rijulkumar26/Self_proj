import numpy as np
from app.config import FAISS_INDEX_PATH, METADATA_PATH, TOP_K

# ----------- GLOBALS (LAZY LOAD) ----------- #
model = None
index = None
metadata = None


# ----------- LOAD RESOURCES LAZILY ----------- #
def load_resources():
    global model, index, metadata

    # Load embedding model
    if model is None:
        from sentence_transformers import SentenceTransformer
        print(" Loading embedding model...")
        model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    # Load FAISS index
    if index is None:
        import faiss
        print(" Loading FAISS index...")
        index = faiss.read_index(FAISS_INDEX_PATH)

    # Load metadata
    if metadata is None:
        import json
        print(" Loading metadata...")
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)


# ----------- EMBED QUERY ----------- #
def embed_query(query):
    load_resources()

    query = f"query: {query}"
    embedding = model.encode(query, normalize_embeddings=True)

    return np.array([embedding]).astype("float32")


# ----------- RETRIEVE DOCUMENTS ----------- #
def retrieve_docs(query):
    load_resources()

    query_vector = embed_query(query)

    distances, indices = index.search(query_vector, TOP_K)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):  # safety check
            results.append(metadata[idx])

    return results
