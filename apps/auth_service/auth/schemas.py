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
    uuid: UUID
    username: Annotated[str, Field(max_length=50)]
    first_name: Annotated[str, Field(max_length=50)]
    last_name: Annotated[str, Field(max_length=50)]
    phone_number: str = Field('+79999999999')
    role: UserRole
    district_id: Optional[Annotated[int, Field(ge=1)]] = None
    group_id: Optional[Annotated[int, Field(ge=1)]] = None


class UserCreateRequestSchema(UserBaseSchema):
    password: Annotated[str, Field(min_length=8, max_length=10)]


class UserCreateSchema(UserBaseSchema):
    password_hash: str


class UserUpdateSchema(BaseModel):
    username: Optional[Annotated[str, Field(max_length=50)]] = None
    first_name: Optional[Annotated[str, Field(max_length=50)]] = None
    last_name: Optional[Annotated[str, Field(max_length=50)]] = None
    phone_number: Optional[str] = Field('+79999999999')
    role: Optional[UserRole] = None
    district_id: Optional[Annotated[int, Field(ge=1)]] = None
    group_id: Optional[Annotated[int, Field(ge=1)]] = None
