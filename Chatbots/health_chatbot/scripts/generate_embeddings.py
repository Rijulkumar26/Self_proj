import os
import json
import faiss
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# ----------- CONFIG ----------- #
INPUT_FILE = "data/processed/final_chunks.json"
INDEX_DIR = "data/embeddings/faiss_index"
METADATA_FILE = os.path.join(INDEX_DIR, "metadata.json")

MODEL_NAME = "BAAI/bge-large-en-v1.5"

os.makedirs(INDEX_DIR, exist_ok=True)


# ----------- LOAD MODEL ----------- #
print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)


# ----------- LOAD DATA ----------- #
def load_chunks():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------- FORMAT TEXT (IMPORTANT FOR BGE) ----------- #
def format_passage(text, section):
    return f"passage: {section}. {text}"


# ----------- GENERATE EMBEDDINGS ----------- #
def generate_embeddings():
    data = load_chunks()

    texts = []
    metadata = []

    print("Preparing texts")

    for item in data:
        formatted_text = format_passage(item["content"], item["section"])
        texts.append(formatted_text)
        metadata.append(item)

    print("---------Generating embeddings----------")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True  # IMPORTANT for cosine similarity
    )

    embeddings = np.array(embeddings).astype("float32")

    # ----------- FAISS INDEX ----------- #
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # cosine similarity

    index.add(embeddings)

    # ----------- SAVE FILES ----------- #
    faiss.write_index(index, os.path.join(INDEX_DIR, "index.faiss"))

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Embeddings + FAISS index saved")


if __name__ == "__main__":
    generate_embeddings()