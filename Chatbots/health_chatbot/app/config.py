import os
from dotenv import load_dotenv

load_dotenv()

FAISS_INDEX_PATH = "data/embeddings/faiss_index/index.faiss"
METADATA_PATH = "data/embeddings/faiss_index/metadata.json"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
TOP_K = 5

if not GOOGLE_API_KEY:
    raise ValueError(" GOOGLE_API_KEY not found in .env file")