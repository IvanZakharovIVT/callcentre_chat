from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from apps.core.models import BaseDBModel


class Message(BaseDBModel):
    __tablename__ = "chat_message"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[Text] = mapped_column(type_=Text)
    user_uid: Mapped[int] = mapped_column( type_=String(36))
    username: Mapped[str] = mapped_column(type_=String(255))
    email: Mapped[str] = mapped_column(type_=String(50))
