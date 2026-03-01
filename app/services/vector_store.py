import faiss
import numpy as np
import os

INDEX_PATH = "app/data/faiss.index"
dimension = 384

# Create base index
base_index = faiss.IndexFlatL2(dimension)
index = faiss.IndexIDMap(base_index)

# Load if exists
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)


def save_index():
    faiss.write_index(index, INDEX_PATH)


def add_vectors(vectors, chunk_ids):
    vectors = np.array(vectors).astype("float32")
    ids = np.array(chunk_ids).astype("int64")

    index.add_with_ids(vectors, ids)
    save_index()


def search(query_vector, top_k=5):
    query_vector = np.array([query_vector]).astype("float32")

    distances, ids = index.search(query_vector, top_k)

    results = []

    for dist, chunk_id in zip(distances[0], ids[0]):
        if chunk_id == -1:
            continue

        results.append({
            "chunk_id": int(chunk_id),
            "score": float(dist)
        })

    return results


def remove_vectors_by_chunk_ids(chunk_ids_to_remove):
    ids = np.array(chunk_ids_to_remove).astype("int64")
    index.remove_ids(ids)
    save_index()