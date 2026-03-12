from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin

from apps.auth_service.admin.admin import UserAdmin
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

app.include_router(auth_router)

# Create admin
admin = Admin(engine, title="Example: SQLAlchemy")

# Add view
admin.add_view(UserAdmin(User))

# Mount admin to your app
admin.mount_to(app)
