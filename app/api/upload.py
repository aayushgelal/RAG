from fastapi import APIRouter, UploadFile, File
from app.models.database import SessionLocal, Document, Chunk
from app.services.chunking import chunk_text
from app.services.embeddings import embed_batch
from app.services.vector_store import add_vectors,remove_vectors_by_chunk_ids
from app.security.sanitizer import sanitize_text
from pypdf import PdfReader

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    db = SessionLocal()

    # ---- Replace document if exists ----
    existing_doc = db.query(Document).filter(
        Document.name == file.filename
    ).first()

    if existing_doc:
        # Get old chunk IDs
        old_chunks = db.query(Chunk).filter(
            Chunk.document_id == existing_doc.id
        ).all()

        old_chunk_ids = [c.id for c in old_chunks]

        # Delete old chunks + document
        db.query(Chunk).filter(
            Chunk.document_id == existing_doc.id
        ).delete()

        db.query(Document).filter(
            Document.id == existing_doc.id
        ).delete()

        db.commit()

        # Remove vectors from FAISS
        remove_vectors_by_chunk_ids(old_chunk_ids)

    # ---- Read File ----
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    else:
        content = await file.read()
        text = content.decode("utf-8")

    # ---- Sanitize ----
    text = sanitize_text(text)

    db = SessionLocal()

    # ---- Save Document ----
    doc = Document(name=file.filename)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # ---- Chunk ----
    chunks = chunk_text(text, chunk_size=80, overlap=20)

    texts = []
    chunk_ids = []

    for chunk in chunks:
        db_chunk = Chunk(
            document_id=doc.id,
            chunk_index=chunk["chunk_index"],
            text=chunk["text"]
        )
        db.add(db_chunk)
        db.commit()
        db.refresh(db_chunk)

        texts.append(chunk["text"])
        chunk_ids.append(db_chunk.id)

    # ---- Embed + Store in FAISS ----
    embeddings = embed_batch(texts)
    add_vectors(embeddings, chunk_ids)

    db.close()

    return {"message": "File uploaded successfully"}