from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def ask_question():
    return {"answer": "This is a placeholder answer."}
