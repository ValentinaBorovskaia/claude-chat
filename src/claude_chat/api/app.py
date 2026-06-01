from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Claude Chat API",
    description="AI chat backend powered by Claude",
    version="0.1.0"
)

app.include_router(router)