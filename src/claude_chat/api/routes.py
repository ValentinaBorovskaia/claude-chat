from fastapi import APIRouter, HTTPException
from anthropic import BadRequestError, APIConnectionError
from pydantic import BaseModel, Field, field_validator
from ..client import ClaudeClient
from ..models import ChatHistory

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    history: list[dict] = Field(default=[], max_length=100)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

    @field_validator("message")
    @classmethod
    def message_strip(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Message cannot be empty or whitespace")
        return stripped

class ChatResponse(BaseModel):
    response: str
    history: list[dict]

router = APIRouter()
client = ClaudeClient()

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