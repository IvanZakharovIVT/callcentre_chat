from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin
from starlette.middleware.sessions import SessionMiddleware

from apps.auth_service.admin.admin import UserAdmin
from apps.auth_service.admin.auth import UsernameAndPasswordProvider
from apps.auth_service.auth.models import User
from apps.auth_service.auth.router import router as auth_router
from apps.core.database import engine

app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    title="auth user swagger",
    version="1.0.0",
)


app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key", # Replace with a strong, random key
    # optional parameters
    # https_only=True,
    # max_age=3600 # seconds until the session expires
)

app.include_router(auth_router)

# Create admin
admin = Admin(engine, auth_provider=UsernameAndPasswordProvider(), title="Example: SQLAlchemy")

# Add view
admin.add_view(UserAdmin(User))

# Mount admin to your app
admin.mount_to(app)
