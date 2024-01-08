import uuid
from datetime import datetime
from pydantic import Field
from typing import List, Optional

from pydantic import BaseModel


class Event(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created: datetime = Field(default_factory=datetime.now)
    content: str
    publisher: str


class Subscription:
    def __init__(self, subscriber, message_type):
        self.subscriber = subscriber
        self.message_type = message_type


class EventTypes:
    def __init__(self) -> None:
        pass
