import anthropic
from .config import settings
from .models import ChatHistory

class ClaudeClient:
    def __init__(self):
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def send(self, history: ChatHistory, system_prompt: str = "") -> str:
        response = self._client.messages.create(
            model=settings.model,
            max_tokens=settings.max_tokens,
            system=system_prompt,
            messages=history.to_api_format()
        )
        return response.content[0].text

    def send_streaming(self, history: ChatHistory, system_prompt: str = "") -> None:
        """Ответ печатается по мере генерации — как в claude.ai"""
        with self._client.messages.stream(
            model=settings.model,
            max_tokens=settings.max_tokens,
            system=system_prompt,
            messages=history.to_api_format()
        ) as stream:
            full_response = ""
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text
            print()
        return full_response