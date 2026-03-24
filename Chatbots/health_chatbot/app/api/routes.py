from fastapi import APIRouter
from app.services.chat_engine import get_answer

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/chat")
def chat(query: str):
    result = get_answer(query)
    return result