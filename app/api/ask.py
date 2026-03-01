from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import generate_answer
from app.services.retreival import retrieve

router = APIRouter()

class AskRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(request: AskRequest):
    chunks = retrieve(request.question)

    answer, citations = generate_answer(request.question, chunks)

    return {
        "answer": answer,
        "citations": citations
    }