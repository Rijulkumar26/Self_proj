import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import FAISS_INDEX_PATH, METADATA_PATH, TOP_K

MODEL_NAME = "BAAI/bge-small-en-v1.5"

# Load once
model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(FAISS_INDEX_PATH)

with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)


def embed_query(query):
    query = f"query: {query}"
    embedding = model.encode(query, normalize_embeddings=True)
    return np.array([embedding]).astype("float32")


def retrieve_docs(query):
    query_vector = embed_query(query)

    distances, indices = index.search(query_vector, TOP_K)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])

    return results
