from typing import Annotated

from fastapi import APIRouter, Depends, Response

from apps.auth_service.auth.schemas import UserCreateRequestSchema, UserAuthSchemaBase
from apps.auth_service.auth.services.auth_service import AuthService
from apps.auth_service.auth.services.cookie_service import CookieService
from apps.core.config import settings
from apps.core.database import AsyncSession, get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign_up")
async def sign_up(
        session: Annotated[AsyncSession, Depends(get_session)],
        signup_schema: UserCreateRequestSchema
):
    await AuthService(session).sign_up(signup_schema)


@router.post(
    '/sign_in',
    summary='Авторизация в системе',
    description='Токены сохраняются в cookie',
)
async def sign_in(
    response: Response,
    credentials_schema: UserAuthSchemaBase,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    auth_service = AuthService(session)
    user = await auth_service.authenticate_and_get_user_jwt(
        credentials_schema.username, credentials_schema.password, session
    )

    subject = {
        'username': user.username,
        'uuid': user.uuid,
        'remember_me': credentials_schema.remember_me,
    }
    CookieService.set_auth_token(subject, response)
    CookieService.set_refresh_token(
        subject, credentials_schema.remember_me, response
    )
    return {'message': 'Successfully logged in'}

@router.post(
    '/logout',
    summary='Выход из системы',
    description='Удаление токенов из cookie',
)
async def logout(
    response: Response,
):
    CookieService.delete_cookie(response, settings.AUTH_TOKEN_NAME)
    CookieService.delete_cookie(response, settings.REFRESH_TOKEN_NAME)
    return {'message': 'Successfully logout'}
