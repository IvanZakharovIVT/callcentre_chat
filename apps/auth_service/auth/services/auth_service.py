from datetime import timedelta
from uuid import uuid4
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response

from apps.auth_service.auth.exceptions import UserAuthorizationError
from apps.auth_service.auth.models import User
from apps.auth_service.auth.repository import UserRepository
from apps.auth_service.auth.schemas import UserCreateRequestSchema, UserCreateSchema
from apps.auth_service.auth.security import refresh_security, access_security
from apps.core.config import settings

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

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    async def authenticate_and_get_user_jwt(
            self, username: str, password: str, session: AsyncSession
    ) -> User:
        user = await self._user_repository.get_by_username(username)
        if not user:
            raise UserAuthorizationError(username)
        hashed_password = self._hash_password(password)
        if hashed_password == user.password_hash:
            return user
        raise UserAuthorizationError(username)

    def _set_token(
            self,
            token: str,
            token_name: str,
            max_age: int,
            response: Response,
    ):
        response.delete_cookie(token_name)
        response.set_cookie(
            key=token_name,
            value=token,
            httponly=True,
            max_age=max_age,
            secure=True,
            samesite='none',
            domain=settings.COOKIE_DOMAIN,
        )

    def set_auth_token(
            self,
            subject: dict,
            response: Response,
    ):
        max_age = settings.AUTH_TOKEN_TIMEDELTA
        auth_token = access_security.create_access_token(
            subject=subject, expires_delta=timedelta(seconds=max_age)
        )
        self._set_token(auth_token, settings.AUTH_TOKEN_NAME, max_age, response)

    def set_refresh_token(
            self,
            subject: dict,
            remember_me: bool,
            response: Response,
    ):
        max_age = settings.REFRESH_TOKEN_TIMEDELTA
        if remember_me:
            max_age = settings.REMEMBER_ME_REFRESH_TIMEDELTA
        refresh_token_val = refresh_security.create_refresh_token(
            subject=subject,
            expires_delta=timedelta(seconds=max_age),
        )
        self._set_token(
            refresh_token_val,
            settings.REFRESH_TOKEN_NAME,
            max_age,
            response,
        )

    def delete_cookie(self, response: Response, cookie_name: str, frontend_domain: str):
        # frontend_domain = convert_front_domain(frontend_domain)
        response.delete_cookie(
            cookie_name,
            httponly=frontend_domain == settings.COOKIE_DOMAIN,
            secure=frontend_domain == settings.COOKIE_DOMAIN,
            domain=frontend_domain
        )
