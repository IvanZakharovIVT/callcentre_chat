from fastapi import HTTPException
from starlette import status


class UserAuthorizationError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, username: str):
        self.username = username

    @property
    def detail(self) -> str:
        return (
            f'Ошибка авторизации для {self.username}. Неверно указан логин или пароль'
        )
