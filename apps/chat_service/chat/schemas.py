from typing import Annotated

from pydantic import BaseModel, Field



class ChatBaseSchema(BaseModel):
    name: Annotated[str, Field(max_length=255)]


class ChatCreateSchema(ChatBaseSchema):
    pass


class ChatUpdateSchema(ChatBaseSchema):
    pass


class ChatDetailSchema(ChatBaseSchema):
    id: int
