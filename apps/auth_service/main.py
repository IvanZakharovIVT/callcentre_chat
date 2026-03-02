from fastapi import FastAPI

from apps.auth_service.auth.router import router as auth_router

app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    title="auth user swagger",
    version="1.0.0",
)

app.include_router(auth_router)
