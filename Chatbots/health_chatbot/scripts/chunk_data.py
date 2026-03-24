import json
import os
from tqdm import tqdm

INPUT_FILE = "data/processed/chunks.json"
OUTPUT_FILE = "data/processed/final_chunks.json"

CHUNK_SIZE = 400        # words per chunk
CHUNK_OVERLAP = 80      # overlap words


def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def split_into_chunks(text, chunk_size, overlap):
    words = text.split()
    chunks = []

    start = 0
    chunk_id = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        chunks.append({
            "chunk_id": chunk_id,
            "content": chunk_text
        })

        chunk_id += 1
        start += chunk_size - overlap   # move with overlap

    return chunks


def process_chunks():
    data = load_data()
    final_chunks = []

    for item in tqdm(data):
        text = item["content"]

        # skip very small content
        if len(text.split()) < 50:
            continue

        chunks = split_into_chunks(
            text,
            CHUNK_SIZE,
            CHUNK_OVERLAP
        )

        for chunk in chunks:
            final_chunks.append({
                "policy_name": item["policy_name"],
                "section": item["section"],
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "source_file": item["source_file"]
            })

    save_data(final_chunks)
    print(f"Saved chunked data to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_chunks()