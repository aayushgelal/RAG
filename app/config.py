import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "data", "app.db")
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "data", "faiss.index")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 100
TOP_K = 3