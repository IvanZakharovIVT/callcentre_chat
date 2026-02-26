from uuid import uuid4
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth_service.auth.exceptions import UserAuthorizationError
from apps.auth_service.auth.models import User
from apps.auth_service.auth.repository import UserRepository
from apps.auth_service.auth.schemas import UserCreateRequestSchema, UserCreateSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._user_repository = UserRepository(session)

    async def sign_up(self, user_base_schema: UserCreateRequestSchema):
        await self._user_repository.create(
            UserCreateSchema(**{
                **user_base_schema.model_dump(),
                "password_hash": self._hash_password(user_base_schema.password),
                "uuid": str(uuid4())
            })
        )
        await self._session.flush()
        await self._session.commit()

    @staticmethod
    def _hash_password(password: str) -> str:
        return pwd_context.hash(password)

    async def authenticate_and_get_user_jwt(
            self, username: str, password: str
    ) -> User:
        user = await self._user_repository.get_by_username(username)
        if not user:
            raise UserAuthorizationError(username)
        if pwd_context.verify(password, user.password_hash):
            return user
        raise UserAuthorizationError(username)
