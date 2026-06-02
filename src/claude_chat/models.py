from pydantic import BaseModel, Field, field_validator
from typing import Literal

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)

class ChatHistory(BaseModel):
    messages: list[Message] = []

    def add(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def to_api_format(self) -> list[dict]:
        return [m.model_dump() for m in self.messages]