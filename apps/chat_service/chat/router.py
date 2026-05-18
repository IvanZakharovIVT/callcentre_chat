from typing import Annotated

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth_service.auth.security import get_data_from_access_token
from apps.chat_service.chat.repository import ChatRepository
from apps.chat_service.chat.schemas import ChatDetailSchema, ChatCreateSchema
from apps.chat_service.chat.services.chat_service import ChatService
from apps.chat_service.message.models import Message
from apps.core.config import settings
from apps.core.database import get_session
from apps.core.schema_base import AuthenticatedUser
from apps.core.services.elasticsearch_service import ElasticsearchService

router = APIRouter(prefix="/chat", tags=["chat"])

es_service = ElasticsearchService()


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


@router.get(
    '/search',
    summary='Поиск сообщений',
    description='Поиск сообщений по содержимому через Elasticsearch с выборкой из БД',
)
async def search_messages(
    q: Annotated[str, Query(description="Поисковый запрос")],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[AuthenticatedUser, Depends(get_data_from_access_token)],
):
    # Search in Elasticsearch
    es_result = await es_service.search(settings.ES_INDEX, q)
    
    # Extract chat_ids from ES hits
    hits = es_result.get("hits", {}).get("hits", [])
    if not hits:
        return {"results": [], "total": 0}
    
    message_ids = list(set(
        hit["_source"].get("message_id") for hit in hits if hit["_source"].get("message_id")
    ))
    
    # Query database for messages in those chats
    stmt = (
        select(Message)
        .where(Message.id.in_(message_ids))
        .order_by(Message.created_at.desc())
    )
    result = await session.execute(stmt)
    messages = result.unique().scalars().all()
    
    return {
        "results": [
            {
                "id": msg.id,
                "content": msg.content,
                "username": msg.username,
                "user_uid": msg.user_uid,
                "email": msg.email,
                "chat_id": msg.chat_id,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
            }
            for msg in messages
        ],
        "total": len(messages),
        "es_total": es_result.get("hits", {}).get("total", {}).get("value", 0),
    }
