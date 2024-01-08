import uuid
from datetime import datetime
from pydantic import Field

from pydantic import BaseModel


class Request(BaseModel):
    content: str


class Response(BaseModel):
    content: str


class Message(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created: datetime = Field(default_factory=datetime.now)
    role: str
    publisher: str
    content: str

    def data_dump(self):
        return {
            "role": self.role,
            "content": self.content,
        }


class UserMessage(Message):
    def __init__(self, content: str, publisher: str):
        super().__init__(role="user", content=content, publisher=publisher)


class AssistantMessage(Message):
    def __init__(self, content: str, publisher: str):
        super().__init__(role="assistant", content=content, publisher=publisher)


class SystemMessage(Message):
    def __init__(self, content: str, publisher: str):
        super().__init__(role="system", content=content, publisher=publisher)
