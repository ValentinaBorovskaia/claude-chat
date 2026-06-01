from fastapi import APIRouter
from pydantic import BaseModel
from ..client import ClaudeClient
from ..models import ChatHistory

router = APIRouter()
client = ClaudeClient()

# Request/Response схемы
class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

class ChatResponse(BaseModel):
    response: str
    history: list[dict]

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    # Восстанавливаем историю из запроса
    history = ChatHistory()
    for msg in request.history:
        history.add(msg["role"], msg["content"])

    # Добавляем новое сообщение
    history.add("user", request.message)

    # Получаем ответ от Claude
    response = client.send(history)

    # Добавляем ответ в историю
    history.add("assistant", response)

    return ChatResponse(
        response=response,
        history=history.to_api_format()
    )