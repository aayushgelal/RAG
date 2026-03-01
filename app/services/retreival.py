from sqlalchemy.orm import joinedload

from app.services.embeddings import embed_text
from app.services.vector_store import search
from app.models.database import SessionLocal, Chunk
from app.config import TOP_K
from app.security.sanitizer import sanitize_text


def keyword_score(text, question):
    score = 0
    question_words = question.lower().split()

    for word in question_words:
        if word in text.lower():
            score += 1

    return score


def retrieve(question: str):
    db = SessionLocal()

    # 1️⃣ Embed query
    query_vector = embed_text(question)

    # 2️⃣ Vector search (get more than needed)
    vector_results = search(query_vector, TOP_K * 3)

    chunk_ids = [r["chunk_id"] for r in vector_results]

    # 🔥 EAGER LOAD DOCUMENT RELATIONSHIP
    chunks = (
        db.query(Chunk)
        .options(joinedload(Chunk.document))
        .filter(Chunk.id.in_(chunk_ids))
        .all()
    )

    # 3️⃣ Combine vector + keyword scoring
    scored_chunks = []

    for chunk in chunks:
        chunk.text = sanitize_text(chunk.text)
        vector_score = next(
            (r["score"] for r in vector_results if r["chunk_id"] == chunk.id),
            9999
        )

        kw_score = keyword_score(chunk.text, question)

        # Lower distance = better → invert
        final_score = (1 / (1 + vector_score)) + (0.2 * kw_score)

        scored_chunks.append((chunk, final_score))

    # 4️⃣ Sort by final score
    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    # 5️⃣ Take top K unique
    final_chunks = []
    seen = set()

    for chunk, _ in scored_chunks:
        if chunk.id not in seen:
            final_chunks.append(chunk)
            seen.add(chunk.id)

        if len(final_chunks) == TOP_K:
            break

    db.close()
    return final_chunks