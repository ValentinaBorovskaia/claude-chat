from fastapi import APIRouter, HTTPException
from anthropic import BadRequestError, APIConnectionError
from pydantic import BaseModel
from ..client import ClaudeClient
from ..models import ChatHistory

router = APIRouter()
client = ClaudeClient()

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
    try:
        history = ChatHistory()
        for msg in request.history:
            history.add(msg["role"], msg["content"])

        history.add("user", request.message)
        response = client.send(history)
        history.add("assistant", response)

        return ChatResponse(
            response=response,
            history=history.to_api_format()
        )
    except BadRequestError as e:
        raise HTTPException(status_code=402, detail="Insufficient API credits")
    except APIConnectionError as e:
        raise HTTPException(status_code=502, detail="Cannot reach Anthropic API")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))