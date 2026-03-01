from fastapi import APIRouter
from app.models.database import SessionLocal, Document, Chunk
from app.services.vector_store import remove_vectors_by_chunk_ids

router = APIRouter()

@router.get("/documents")
def list_documents():
    db = SessionLocal()
    docs = db.query(Document).all()

    results = [
        {"id": doc.id, "name": doc.name}
        for doc in docs
    ]

    db.close()
    return results


@router.delete("/documents/{doc_id}")
def delete_document(doc_id: int):
    db = SessionLocal()

    chunks = db.query(Chunk).filter(Chunk.document_id == doc_id).all()
    chunk_ids = [c.id for c in chunks]

    db.query(Chunk).filter(Chunk.document_id == doc_id).delete()
    db.query(Document).filter(Document.id == doc_id).delete()

    db.commit()
    db.close()

    # Remove from FAISS (simple rebuild strategy)
    remove_vectors_by_chunk_ids(chunk_ids)

    return {"message": "Document deleted successfully"}