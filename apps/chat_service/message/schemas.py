from typing import Annotated

from pydantic import BaseModel, Field



class MessageBaseSchema(BaseModel):
    content: str
    user_uid: str
    username: str
    email: str


class MessageCreateSchema(MessageBaseSchema):
    pass


class MessageUpdateSchema(MessageBaseSchema):
    pass


class MessageDetailSchema(MessageBaseSchema):
    pass

