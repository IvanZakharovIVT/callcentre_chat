import asyncio
from typing import Annotated

from fastapi import Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from apps.auth_service.auth.security import get_data_from_socket_access_token
from apps.chat_service.chat.router import router
from apps.chat_service.message.services.message_service import MessageService
from apps.core.database import get_session
from apps.core.managers.connection_manager import connection_manager
from apps.core.schema_base import AuthenticatedUser


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
