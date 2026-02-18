from sqlalchemy.orm import Mapped, mapped_column

from apps.core.models import BaseDBModel


class Chat(BaseDBModel):
    __tablename__ = "chat_chat"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
