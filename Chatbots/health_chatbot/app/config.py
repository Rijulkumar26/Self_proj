import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAISS_INDEX_PATH = os.path.join(BASE_DIR, "../data/embeddings/faiss_index/index.faiss")
METADATA_PATH = os.path.join(BASE_DIR, "../data/embeddings/faiss_index/metadata.json")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
TOP_K = 5

if not GOOGLE_API_KEY:
    raise ValueError(" GOOGLE_API_KEY not found in .env file")
