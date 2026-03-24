from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API working"}

@router.post("/chat")
def chat(query: str):
    from app.services.chat_engine import get_answer  # for lazy import

    return get_answer(query)
