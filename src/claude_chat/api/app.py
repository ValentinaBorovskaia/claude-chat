import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

# Настройка логгера — аналог ILogger в .NET
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Claude Chat API",
    description="AI chat backend powered by Claude",
    version="0.1.0"
)

# CORS middleware — разрешаем запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде сюда ставят конкретный домен
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # До эндпоинта
    logger.info(f"→ {request.method} {request.url.path}")

    response = await call_next(request)  # вызываем эндпоинт

    # После эндпоинта
    duration = round((time.time() - start_time) * 1000)
    logger.info(f"← {response.status_code} {request.url.path} {duration}ms")

    return response

app.include_router(router)