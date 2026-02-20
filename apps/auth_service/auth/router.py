from typing import Annotated

from fastapi import APIRouter, Depends

from apps.auth_service.auth.schemas import UserCreateRequestSchema
from apps.auth_service.auth.services.auth_service import AuthService
from apps.core.database import AsyncSession, get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign_up")
async def sign_up(
        session: Annotated[AsyncSession, Depends(get_session)],
        signup_schema: UserCreateRequestSchema
):
    await AuthService(session).sign_up(signup_schema)