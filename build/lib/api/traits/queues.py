import json
import asyncio
from typing import Any, Callable

import redis

from scint.api.types import Trait


class Processable(Trait):
    async def process(self, handler):
        self.loop = asyncio.get_event_loop()
        self.queue = redis.Redis(host="localhost", port=6379, db=0)
        self.processing = False

    def put(self, obj: Any):
        try:
            self.queue.lpush(self.name, obj.model_dump_json())
        except Exception as e:
            print(e)
            return False
        finally:
            return True

    def get(self):
        message = self.queue.rpop(self.name)
        if message:
            return json.loads(message)
        return None


class Sendable(Trait):
    def put(self, obj: Any):
        try:
            self.loop.call_soon_threadsafe(self.queue.put_nowait, obj)
        except Exception as e:
            print(e)
            return False
        finally:
            return True

    def get(self, obj: Any):
        self.queue.get_nowait(obj)

    async def receive(self) -> Any:
        return await self.queue.get()

    async def start(self, handler: Callable):
        self.handler = handler
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.processing = False

        while self._running:
            message = await self.receive()
            await handler(message)

    async def stop(self):
        self._running = False


class Waitable(Trait):
    def enque(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            message = args[0]
            self.queue.lpush(self.name, json.dumps(message))
            return True
        elif args or kwargs:
            return self.__init__(*args, **kwargs)
        return self

    def deque(self, *args, **kwargs):
        if args or kwargs:
            return self.__init__(*args, **kwargs)
        message = self.queue.rpop(self.name)
        if message:
            return json.loads(message)
        return None
