from typing import Optional, Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from apps.auth_service.auth.enums import UserRole


class SighUpSchema(BaseModel):
    username: str
    email: str
    role: UserRole
    password: str


class UserBaseSchema(BaseModel):
    username: Annotated[str, Field(max_length=50)]
    email: Annotated[str, Field(max_length=50)]
    role: UserRole


class UserCreateRequestSchema(UserBaseSchema):
    password: Annotated[str, Field(min_length=8, max_length=10)]


class UserCreateSchema(UserBaseSchema):
    uuid: UUID
    password_hash: str


class UserUpdateSchema(BaseModel):
    username: Optional[Annotated[str, Field(max_length=50)]] = None
    role: Optional[UserRole] = None
