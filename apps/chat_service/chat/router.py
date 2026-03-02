import asyncio
from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from apps.auth_service.auth.security import get_data_from_access_token
from apps.chat_service.chat.repository import ChatRepository
from apps.chat_service.chat.schemas import ChatDetailSchema, ChatCreateSchema
from apps.chat_service.chat.services.chat_service import ChatService
from apps.core.database import get_session
from apps.core.managers.connection_manager import connection_manager

router = APIRouter(prefix="/chat", tags=["chat"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("websocket")
    await connection_manager.connect(1, 1, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            # await connection_manager.send_message(f"Сообщение: {data}", websocket)
            await asyncio.sleep(3)
            await connection_manager.broadcast(1, f"Сообщение: {data}", websocket)
    except WebSocketDisconnect:
        connection_manager.disconnect(1, 1)

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
async def create_station(
    chat_schema: ChatCreateSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[dict, Depends(get_data_from_access_token)],
):
    service = ChatService(session)
    new_chat = await service.create_chat(chat_schema)
    chat_id = new_chat.id
    await session.commit()
    return await ChatRepository(session).get_by_pk(chat_id)
