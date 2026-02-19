from fastapi import FastAPI

from apps.chat_service.chat.router import router as chat_router

app = FastAPI(
    root_path="/api/chat",
    # openapi_url="/openapi.json",
    title="web_chat",
    version="1.0.0",
    # openapi_version="3.1.0"
)

app.include_router(chat_router)
