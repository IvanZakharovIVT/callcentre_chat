from typing import Annotated

from fastapi import APIRouter, Depends, Response

from apps.auth_service.auth.schemas import UserCreateRequestSchema, UserAuthSchemaBase
from apps.auth_service.auth.services.auth_service import AuthService
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
    set_auth_token(subject, response)
    set_refresh_token(
        subject, credentials_schema.remember_me, response
    )
    response.raw_headers = [
        (item[0], item[1] + b';Partitioned') for item in response.headers.raw
    ]
    return {'message': 'Successfully logged in'}