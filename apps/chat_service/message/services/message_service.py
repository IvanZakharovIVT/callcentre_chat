from sqlalchemy.ext.asyncio import AsyncSession

from apps.chat_service.message.repository import MessageRepository
from apps.chat_service.message.schemas import MessageCreateSchema, MessageDetailSchema


class MessageService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = MessageRepository(session)

    async def save_message(self, message: dict) -> MessageDetailSchema:
        schema = MessageCreateSchema(**message)
        message_obj = await self._repository.create(schema)
        schema = MessageDetailSchema.model_validate(message_obj, from_attributes=True)
        await self._session.commit()
        return schema
