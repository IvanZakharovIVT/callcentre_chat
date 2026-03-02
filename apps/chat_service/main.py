from fastapi import FastAPI

from apps.chat_service.chat.router import router as chat_router

app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    title="web_chat",
    version="1.0.0",
)

app.include_router(chat_router)
