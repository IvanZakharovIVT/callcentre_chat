from sqlalchemy.ext.asyncio import AsyncSession

from apps.chat_service.chat.repository import ChatRepository
from apps.chat_service.chat.schemas import ChatCreateSchema


class ChatService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = ChatRepository(session)

    async def create_chat(self, chat: ChatCreateSchema):
        chat = await self._repository.create(chat)
        return chat
