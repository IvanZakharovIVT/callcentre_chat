from sqlalchemy.ext.asyncio import AsyncSession

from apps.chat_service.message.models import Message
from apps.chat_service.message.schemas import MessageCreateSchema, MessageUpdateSchema
from apps.core.repository_base import BaseRepository


class MessageRepository(BaseRepository[Message, MessageCreateSchema, MessageUpdateSchema]):
    def __init__(self, session: AsyncSession):
        self.model = Message
        super().__init__(session)
