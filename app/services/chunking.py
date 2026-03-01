from app.config import CHUNK_SIZE,CHUNK_OVERLAP

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    start = 0
    index = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunks.append({
            "chunk_index": index,
            "text": chunk_text
        })

        start += chunk_size - overlap
        index += 1

    return chunks