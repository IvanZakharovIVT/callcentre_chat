from pydantic import BaseModel

from apps.auth_service.auth.enums import UserRoles


class SighUpSchema(BaseModel):
    username: str
    email: str
    role: UserRoles
    password: str