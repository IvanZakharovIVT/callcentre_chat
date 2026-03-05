from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.core.models import BaseDBModel


class Chat(BaseDBModel):
    __tablename__ = "chat_chat"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    messages: Mapped[Optional["Message"]] = relationship("Message", back_populates="chat")