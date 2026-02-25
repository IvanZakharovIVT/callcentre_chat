from typing import Optional, Annotated

from pydantic import BaseModel, Field

from apps.auth_service.auth.enums import UserRole


class UserAuthSchemaBase(BaseModel):
    username: Annotated[str, Field(max_length=50)]
    password: Annotated[str, Field(min_length=8, max_length=20)]
    remember_me: Optional[bool] = True


class UserBaseSchema(BaseModel):
    username: Annotated[str, Field(max_length=50)]
    email: Annotated[str, Field(max_length=50)]
    role: UserRole


class UserCreateRequestSchema(UserBaseSchema):
    password: Annotated[str, Field(min_length=8, max_length=20)]


class UserCreateSchema(UserBaseSchema):
    uuid: str
    password_hash: str


class UserUpdateSchema(BaseModel):
    username: Optional[Annotated[str, Field(max_length=50)]] = None
    role: Optional[UserRole] = None
