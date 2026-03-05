from typing import Optional

from sqlalchemy import Text, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.chat_service.chat.models import Chat
from apps.core.models import BaseDBModel


class Message(BaseDBModel):
    __tablename__ = "chat_message"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[Text] = mapped_column(type_=Text)
    user_uid: Mapped[int] = mapped_column( type_=String(36))
    username: Mapped[str] = mapped_column(type_=String(50))
    email: Mapped[str] = mapped_column(type_=String(50))
    chat_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey(Chat.id, ondelete="SET NULL"),
        nullable=True
    )
    chat: Mapped[Optional["Chat"]] = relationship(
        'Chat',
        foreign_keys='Message.chat_id',
        back_populates='messages',
    )