from functools import lru_cache
from typing import Any, Dict

from pydantic import model_validator
from pydantic_settings import BaseSettings

from apps.core.exeptions import MissingEnvVar


class Settings(BaseSettings):
    # COMMON CONFIG
    TITLE: str = 'None-Titled'
    DEBUG: bool = True
    ALLOWED_HOSTS: list[str] = ['*']
    LOG_LEVEL: str = 'INFO'
    TIMEZONE: str = 'UTC'

    # DATABASE CONFIG
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # API VERSION CONFIG
    API_V1: str = '/v1'

    # JWT TOKEN
    TOKEN_SECURE: bool = False
    JWT_SECRET_KEY: str
    AUTH_TOKEN_TIMEDELTA: int = 24 * 60 * 60  # 1 день
    REFRESH_TOKEN_TIMEDELTA: int = 2 * 24 * 60 * 60  # 2 дня
    REMEMBER_ME_REFRESH_TIMEDELTA: int = 4 * 24 * 60 * 60
    AUTH_TOKEN_NAME: str = 'access_token'
    REFRESH_TOKEN_NAME: str = 'refresh_token'
    COOKIE_DOMAIN: str | None = None

    # COMPUTER FIELDS
    @property
    def DATABASE_URL(self) -> str:
        return (
            f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    @property
    def DATABASE_A_URL(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    # Валидация полей
    @model_validator(mode='before')
    @classmethod
    def validate_and_set_defaults(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        for field_name, field in cls.model_fields.items():
            value = data.get(field_name)

            if field.is_required():
                if not value or (isinstance(value, str) and value.strip() == ''):
                    raise MissingEnvVar(
                        f"Поле '{field_name}' обязательно в .env и не может быть пустым"
                    )

            if value is None or (isinstance(value, str) and value.strip() == ''):
                if not field.is_required():
                    data[field_name] = field.default

        return data

    class Config:
        env_file = '.env'
        env_parse_protocol = 'plain'


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
