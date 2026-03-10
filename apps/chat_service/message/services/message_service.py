from sqlalchemy.ext.asyncio import AsyncSession

from apps.chat_service.message.repository import MessageRepository
from apps.chat_service.message.schemas import MessageCreateSchema


class MessageService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = MessageRepository(session)

    async def save_message(self, message: dict):
        schema = MessageCreateSchema(**message)
        await self._repository.create(schema)
        await self._session.commit()
