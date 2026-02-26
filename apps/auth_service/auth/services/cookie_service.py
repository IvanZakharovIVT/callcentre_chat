from datetime import timedelta

from fastapi import Response

from apps.auth_service.auth.security import refresh_security, access_security
from apps.core.config import settings


class CookieService:

    @staticmethod
    def _set_token(
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

    @staticmethod
    def set_auth_token(
            subject: dict,
            response: Response,
    ):
        max_age = settings.AUTH_TOKEN_TIMEDELTA
        auth_token = access_security.create_access_token(
            subject=subject, expires_delta=timedelta(seconds=max_age)
        )
        CookieService._set_token(auth_token, settings.AUTH_TOKEN_NAME, max_age, response)

    @staticmethod
    def set_refresh_token(
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
        CookieService._set_token(
            refresh_token_val,
            settings.REFRESH_TOKEN_NAME,
            max_age,
            response,
        )

    @staticmethod
    def delete_cookie(response: Response, cookie_name: str):
        response.delete_cookie(
            cookie_name,
            httponly=True,
            secure=True,
            domain=settings.COOKIE_DOMAIN
        )