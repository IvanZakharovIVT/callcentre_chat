from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth_service.auth.models import User
from apps.auth_service.auth.schemas import UserCreateSchema, UserUpdateSchema
from apps.core.repository_base import BaseRepository


class UserRepository(BaseRepository[User, UserCreateSchema, UserUpdateSchema]):
    pk_name = 'uid'

    def __init__(self, session: AsyncSession):
        super().__init__(session)
