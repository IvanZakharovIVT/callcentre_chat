from authlib.jose import jwt
from authlib.jose.errors import BadSignatureError, ExpiredTokenError
from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.security import HTTPBasic
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer
from starlette.websockets import WebSocket

from apps.auth_service.auth.exceptions import UserAuthorizationError
from apps.core.config import settings
from apps.core.schema_base import AuthenticatedUser

access_security = JwtAccessBearer(secret_key=settings.JWT_SECRET_KEY, auto_error=True)
refresh_security = JwtRefreshBearer(secret_key=settings.JWT_SECRET_KEY, auto_error=True)


basic_security = HTTPBasic()


async def get_data_from_token(token: str) -> AuthenticatedUser:
    if token:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            payload.validate()
            return AuthenticatedUser(**payload.get('subject', {}))
        except ExpiredTokenError:
            raise HTTPException(
                status_code=401, detail='Срок действия токена закончился'
            )
        except (UserAuthorizationError, BadSignatureError):
            raise HTTPException(
                status_code=401, detail='Invalid token or expired token'
            )
    raise HTTPException(status_code=401, detail='Not authenticated')


async def get_data_from_socket_access_token(websocket: WebSocket) -> AuthenticatedUser:
    return await get_data_from_token(websocket.cookies.get(settings.AUTH_TOKEN_NAME))


async def get_data_from_access_token(request: Request) -> AuthenticatedUser:
    return await get_data_from_token(request.cookies.get(settings.AUTH_TOKEN_NAME))


async def get_data_from_refresh_token(request: Request) -> AuthenticatedUser:
    return await get_data_from_token(request.cookies.get(settings.REFRESH_TOKEN_NAME))
