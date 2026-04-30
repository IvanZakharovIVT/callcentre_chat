from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from apps.core.models import BaseDBModel


class User(BaseDBModel):
    __tablename__ = "auth_user"

    uuid: Mapped[str] = mapped_column(primary_key=True, type_=String(36))
    username: Mapped[str] = mapped_column(type_=String(50))
    email: Mapped[str] = mapped_column(unique=True, index=True, type_=String(50))
    password_hash: Mapped[str] = mapped_column(type_=String(255))
    role: Mapped[str] = mapped_column(primary_key=True, type_=String(30))
    is_online: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_activity_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
