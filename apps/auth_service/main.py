from fastapi import FastAPI

from apps.auth_service.auth.router import router as auth_router

app = FastAPI(
    root_path="/api/user",
    # openapi_url="/openapi.json",
    title="auth user swagger",
    version="1.0.0",
    # openapi_version="3.1.0"
)

app.include_router(auth_router)
