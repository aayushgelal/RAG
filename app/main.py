from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import init_db
from app.api import upload, ask, documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(documents.router)

@app.get("/")
def root():
    return {"message": "RAG App Running"}