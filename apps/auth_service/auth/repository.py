from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth_service.auth.models import User
from apps.auth_service.auth.schemas import UserCreateSchema, UserUpdateSchema
from apps.core.repository_base import BaseRepository


class UserRepository(BaseRepository[User, UserCreateSchema, UserUpdateSchema]):
    pk_name = 'uuid'

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = User

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(select(User).filter_by(username=username))
        return result.unique().scalar_one_or_none()
