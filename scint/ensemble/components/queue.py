import json
from typing import List

from scint.ensemble.traits.base import Trait
from scint.repository.models.message import Message


class Dequeue(Trait):
    def __init__(self):
        self.queue = None
        self.name = None

    def dequeue(self, *args, **kwargs):
        if args or kwargs:
            return self.__init__(*args, **kwargs)
        message = self.queue.rpop(self.name)
        if message:
            return json.loads(message)
        return None


class Enqueue(Trait):
    def __init__(self):
        self.queue = None
        self.name = None
        self.name = None
        self.queue = None

    def enqueue(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            message = args[0]
            self.queue.lpush(self.name, json.dumps(message))
            return True
        elif args or kwargs:
            return self.__init__(*args, **kwargs)
        return self


class Queue(Enqueue, Dequeue):
    enqueued: List[Message] = []
    dequeued: List[Message] = []
