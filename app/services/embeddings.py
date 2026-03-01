from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL_NAME

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def embed_text(text: str):
    return model.encode(text)

def embed_batch(texts):
    return model.encode(texts)