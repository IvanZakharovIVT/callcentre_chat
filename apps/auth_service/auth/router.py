from typing import Annotated

from fastapi import APIRouter, Depends

from apps.core.database import AsyncSession, get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign_up")
async def sign_up(session: Annotated[AsyncSession, Depends(get_session)],):
    ...