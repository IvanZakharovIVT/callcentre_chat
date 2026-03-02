from sqlalchemy.ext.asyncio import AsyncSession

from apps.chat_service.chat.models import Chat
from apps.chat_service.chat.schemas import ChatCreateSchema, ChatUpdateSchema
from apps.core.repository_base import BaseRepository


class ChatRepository(BaseRepository[Chat, ChatCreateSchema, ChatUpdateSchema]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Chat
