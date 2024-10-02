import json

import redis

from scint.framework.components import Component


class Queue(Component):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = redis.Redis(host="localhost", port=6379, db=0)


class Dequeue(Component):
    def deque(self, *args, **kwargs):
        if args or kwargs:
            return self.__init__(*args, **kwargs)
        message = self.queue.rpop(self.name)
        if message:
            return json.loads(message)
        return None


class Enqueue(Component):
    def enque(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            message = args[0]
            self.queue.lpush(self.name, json.dumps(message))
            return True
        elif args or kwargs:
            return self.__init__(*args, **kwargs)
        return self
