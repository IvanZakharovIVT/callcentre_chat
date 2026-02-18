from sqlalchemy import TIMESTAMP, Column, Integer, func

from apps.core.database import Base


class BaseDBModel(Base):
    __abstract__ = True

    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    modified_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
