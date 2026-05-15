import asyncio
from datetime import datetime
from typing import Annotated

from fastapi import Depends, APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from apps.auth_service.auth.security import get_data_from_socket_access_token
from apps.chat_service.message.services.message_service import MessageService
from apps.core.config import settings
from apps.core.database import get_session
from apps.core.managers.connection_manager import connection_manager
from apps.core.schema_base import AuthenticatedUser
from apps.core.services.elasticsearch_service import ElasticsearchService
from apps.chat_service.lifespan import kafka_producer


router = APIRouter(prefix="/message", tags=["message"])

es_service = ElasticsearchService()


@router.websocket("/ping")
async def ping(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("pong")


@router.websocket("/chat/{chat_id}/send")
async def websocket_endpoint(
        websocket: WebSocket,
        current_user: Annotated[AuthenticatedUser, Depends(get_data_from_socket_access_token)],
        chat_id: int
):

    # Send user connected event to Kafka
    try:
        connected_event = {
            "event_type": "user_connected",
            "user_uuid": current_user.uuid,
            "username": current_user.username,
            "timestamp": datetime.utcnow().isoformat()
        }
        await kafka_producer.send_message("user-connected", connected_event)
        print(f"Sent user connected event for {current_user.uuid}")
    except Exception as e:
        print(f"Failed to send user connected event: {e}")
    
    await connection_manager.connect(chat_id, current_user.uuid, websocket)
    try:
        while True:
            message = await websocket.receive_text()
            print(message)
            
            # Send user activity event to Kafka
            try:
                activity_event = {
                    "event_type": "user_activity",
                    "user_uuid": current_user.uuid,
                    "username": current_user.username,
                    "timestamp": datetime.utcnow().isoformat()
                }
                await kafka_producer.send_message("user-activity", activity_event)
            except Exception as e:
                print(f"Failed to send user activity event: {e}")
            
            async for session in get_session():
                data = {
                    'content': message,
                    'user_uid': current_user.uuid,
                    'username': current_user.username,
                    'email': 'current_user',
                    'chat_id': chat_id
                }
                await MessageService(session).save_message(data)

            # Index message in Elasticsearch
            try:
                es_document = {
                    "content": message,
                    "username": current_user.username,
                    "user_uuid": current_user.uuid,
                    "chat_id": chat_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
                await es_service.add_document(settings.ES_INDEX, es_document)
                print(f"Indexed message in Elasticsearch for chat {chat_id}")
            except Exception as e:
                print(f"Failed to index message in Elasticsearch: {e}")

            await connection_manager.broadcast(chat_id, f"Сообщение: {message}", exclude_user=current_user.uuid)
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        # Send user disconnected event to Kafka
        try:
            disconnected_event = {
                "event_type": "user_disconnected",
                "user_uuid": current_user.uuid,
                "username": current_user.username,
                "timestamp": datetime.utcnow().isoformat()
            }
            await kafka_producer.send_message("user-disconnected", disconnected_event)
            print(f"Sent user disconnected event for {current_user.uuid}")
        except Exception as e:
            print(f"Failed to send user disconnected event: {e}")
        
        connection_manager.disconnect(chat_id, current_user.uuid)
