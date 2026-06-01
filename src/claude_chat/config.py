from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    model: str = "claude-opus-4-5"
    max_tokens: int = 1024

    model_config = {"env_file": ".env"}

# Создаём один экземпляр — импортируем везде
settings = Settings()