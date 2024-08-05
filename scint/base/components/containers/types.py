import inspect
from types import SimpleNamespace
from typing import Any, Dict

from pydantic import BaseModel
from typing import Any, List
import json

from redis.asyncio import Redis

from asyncio import Queue

from scint.base.components.prompts.prompts import Message


class Model(BaseModel): ...


class Block(Model):
    type: str = "str"
    data: str

    def build(self):
        return self.data


class ContainerType(type):
    def __new__(cls, name, bases, dct, **kwargs):

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            return getattr(obj.container, self.name)

        def __set__(self, obj, value):
            setattr(obj.container, self.name, value)

        def __delete__(self, obj):
            delattr(obj.container, self.name)

        dct["unpack"] = cls.unpack
        if name == "Container" and dct.get("__module__") == __name__:
            return super().__new__(cls, name, bases, dct)
        return SimpleNamespace(**dct)

    def unpack(self, parent):
        for name, value in inspect.getmembers(self):
            if not name.startswith("__") and name != "assign_to_parent":
                if inspect.ismethod(value) or inspect.isfunction(value):
                    setattr(parent, name, value.__func__.__get__(parent))
                else:
                    setattr(parent, name, value)


class Container(metaclass=ContainerType):
    pass


class Task: ...


class Tasks: ...


class Queue:
    def __init__(self, owner, name):
        self.redis = Redis(host="localhost", port=6379)
        self.owner = owner
        self.name = name

    async def push(self, obj):
        obj = obj.model_dump_json()
        await self.redis.lpush(self.name, obj)

    async def pop(self):
        result = await self.redis.rpop(self.name)
        if result:
            return Message(**json.loads(result))
        return None

    async def has_messages(self):
        length = await self.redis.llen(self.name)
        return length > 0


class Queues:
    def __init__(self, other, queues=None):
        for queue in queues:
            setattr(self, queue, self._create_queue_instance(other, queue))

    def _create_queue_instance(self, other, queue):
        return Queue(other, queue)

    class TaskQueue:
        def __init__(self):
            self.queue = Queue()

        async def enqueue(self, task: Task):
            await self.queue.put(task)

        async def dequeue(self):
            return await self.queue.get()

        def task_done(self):
            self.queue.task_done()
