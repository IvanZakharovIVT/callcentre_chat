import asyncio
from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from apps.auth_service.auth.security import get_data_from_access_token, get_data_from_token, \
    get_data_from_socket_access_token
from apps.chat_service.chat.repository import ChatRepository
from apps.chat_service.chat.schemas import ChatDetailSchema, ChatCreateSchema
from apps.chat_service.chat.services.chat_service import ChatService
from apps.chat_service.message.services.message_service import MessageService
from apps.core.config import settings
from apps.core.database import get_session
from apps.core.managers.connection_manager import connection_manager
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


@router.websocket("/{chat_id}/send")
async def websocket_endpoint(
        websocket: WebSocket,
        current_user: Annotated[AuthenticatedUser, Depends(get_data_from_socket_access_token)],
        chat_id: int
):
    print(current_user)
    await connection_manager.connect(chat_id, current_user.uuid, websocket)
    try:
        while True:
            message = await websocket.receive_text()
            print(message)
            async for session in get_session():
                data = {
                    'content': message,
                    'user_uid': current_user.uuid,
                    'username': current_user.username,
                    'email': 'current_user',
                    'chat_id': chat_id
                }
                await MessageService(session).save_message(data)
            await connection_manager.broadcast(chat_id, f"Сообщение: {message}", exclude_user=current_user.uuid)
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        connection_manager.disconnect(chat_id, current_user.uuid)
