from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from apps.core.models import BaseDBModel


class User(BaseDBModel):
    __tablename__ = "auth_user"

    uuid: Mapped[str] = mapped_column(primary_key=True, type_=String(36))
    username: Mapped[str] = mapped_column(type_=String(50))
    email: Mapped[str] = mapped_column(unique=True, index=True, type_=String(50))
    password_hash: Mapped[Text] = mapped_column(type_=String(255))
    role: Mapped[str] = mapped_column(primary_key=True, type_=String(30))
