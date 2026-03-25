from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth_service.auth.security import get_data_from_access_token
from apps.chat_service.chat.repository import ChatRepository
from apps.chat_service.chat.schemas import ChatDetailSchema, ChatCreateSchema
from apps.chat_service.chat.services.chat_service import ChatService
from apps.core.database import get_session
from apps.core.schema_base import AuthenticatedUser

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/ping")
async def ping():
    return {"ping": "pong"}


@router.post(
    '/chat',
    summary='Создание чата',
    description='Создание станции',
    status_code=status.HTTP_201_CREATED,
    response_model=ChatDetailSchema,
)
async def create_chat(
    chat_schema: ChatCreateSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[AuthenticatedUser, Depends(get_data_from_access_token)],
):
    service = ChatService(session)
    new_chat = await service.create_chat(chat_schema)
    chat_id = new_chat.id
    await session.commit()
    return await ChatRepository(session).get_by_pk(chat_id)
