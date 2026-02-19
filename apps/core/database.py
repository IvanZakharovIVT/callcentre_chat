from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from .config import settings


engine = create_async_engine(
    settings.DATABASE_A_URL,
    pool_use_lifo=True,
    pool_pre_ping=True,
)

AsyncSession = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

metadata = MetaData(info={'is_tracked': True})
Base = declarative_base(metadata=metadata)


async def get_session():
    async with AsyncSession() as session:
        try:
            yield session
        finally:
            await session.close()
