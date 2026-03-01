# Retrieval-Augmented Generation (RAG) Application

## Overview

This project implements a full Retrieval-Augmented Generation (RAG) pipeline using:

- FastAPI (Backend API)
- SQLite (Metadata Storage)
- FAISS (Vector Search)
- Sentence-Transformers (Embeddings)
- Gemini API (LLM for answer generation)
- Streamlit (Frontend UI)

The system allows users to:

- Upload documents (TXT, MD, PDF)
- Automatically chunk and embed them
- Store embeddings in FAISS
- Ask questions about uploaded documents
- Receive answers with citations
- View retrieved source chunks

The assistant answers strictly from retrieved documents.

---

## Features

### UI (Streamlit)

- Upload TXT / MD / PDF documents
- Document list with delete option
- Chat interface
- Answers with citations:
- "Show Sources" expandable section
- Streaming-style response display

---

### Backend (FastAPI)

#### Ingestion Pipeline
1. File upload
2. Text extraction (PDF supported)
3. Chunking with overlap
4. Embedding generation
5. Vector storage (FAISS)
6. Metadata storage (SQLite)

#### Retrieval
- Hybrid retrieval:
- Vector similarity (FAISS)
- Keyword scoring
- Top-K reranking
- Deduplication

#### Answer Generation
- Gemini API used for final answer generation
- Context strictly limited to retrieved chunks
- Citations automatically attached

#### Guardrails
- Basic prompt injection detection
- Ignores malicious instructions inside documents

---


## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- FAISS
- Sentence-Transformers (all-MiniLM-L6-v2)
- Google Gemini API
- Streamlit

---

## Demo Video

[📹 Watch Demo Here](https://drive.google.com/file/d/1tzDGHM9U2-j4gVA6xmOeaBRziZ25i6Z7/view?usp=sharing)