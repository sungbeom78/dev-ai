from fastapi import APIRouter
from app.schemas.ask import AskRequest, AskResponse
from app.rag.answer_generator import AnswerGenerator

router = APIRouter()
generator = AnswerGenerator()

@router.post("", response_model=AskResponse)
def ask_question(request: AskRequest):
    result = generator.generate(question=request.question, limit=request.limit)
    return AskResponse(**result)
