from pydantic import BaseModel



class MessageBaseSchema(BaseModel):
    content: str


class MessageCreateSchema(MessageBaseSchema):
    user_uid: str
    username: str
    email: str
    chat_id: int


class MessageUpdateSchema(MessageBaseSchema):
    pass


class MessageDetailSchema(MessageCreateSchema):
    pass

