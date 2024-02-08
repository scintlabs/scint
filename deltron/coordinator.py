from typing import Deque
from deltron.data.models import (
    DataMessage,
    Message,
    SystemMessage,
    SearchMessage,
    UserMessage,
)


class RequestQueue:
    def __init__(self):
        self.requests: Deque[Message]

    def enqueue(self, message: Message):
        self.requests.append(message)

    def dequeue(self, message: Message):
        pass


class Coordinator:
    def __init__(self):
        self.process_queue = RequestQueue()
        self.message_queue = RequestQueue()

    async def generate_response(self, message: UserMessage):
        if isinstance(message, UserMessage):
            self.message_queue.enqueue(message)

    async def search_datastore(self, message: DataMessage):
        if isinstance(message, DataMessage):
            self.process_queue.enqueue(message)

    async def process_data(self, message: SearchMessage):
        if isinstance(message, DataMessage):
            self.process_queue.enqueue(message)
