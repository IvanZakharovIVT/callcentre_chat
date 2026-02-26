import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError
from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.security import HTTPBasic
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer

from apps.auth_service.auth.exceptions import UserAuthorizationError
from apps.core.config import settings

access_security = JwtAccessBearer(secret_key=settings.JWT_SECRET_KEY, auto_error=True)
refresh_security = JwtRefreshBearer(secret_key=settings.JWT_SECRET_KEY, auto_error=True)


basic_security = HTTPBasic()


async def get_data_from_token(request: Request, token_name: str):
    token = request.cookies.get(token_name)
    if token:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            payload.validate()
            return payload.get('subject', {})
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Срок действия токена закончился'
            )
        except (UserAuthorizationError, InvalidSignatureError, InvalidTokenError):
            raise HTTPException(
                status_code=401, detail='Invalid token or expired token'
            )
    raise HTTPException(status_code=401, detail='Not authenticated')


async def get_data_from_access_token(request: Request):
    return await get_data_from_token(request, settings.AUTH_TOKEN_NAME)


async def get_data_from_refresh_token(request: Request):
    return await get_data_from_token(request, settings.REFRESH_TOKEN_NAME)
