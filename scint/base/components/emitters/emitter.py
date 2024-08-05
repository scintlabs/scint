import asyncio
import json
from functools import wraps

import redis.asyncio as redis
from falcon.errors import WebSocketServerError

from scint.base.components.containers.types import Queues
from ..functions.function import Functions

from ..containers import Queue
from ..functions.function import Function
from scint.base.components.prompts.prompts import Message, Messages
from scint.base.requests.process import process_request
from scint.base.requests.schema import Request
from scint.base.utils import generate_id


class EmitterType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        def _event_emitter(func):
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                print(f"Calling method: {func.__name__}")
                return func(*args, **kwargs)

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                print(f"Calling async method: {func.__name__}")
                return await func(*args, **kwargs)

            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper

        for attr_name, attr_value in dct.items():
            if callable(attr_value):
                dct[attr_name] = _event_emitter(attr_value)

        def _build(self):
            return Request(
                **{
                    "messages": self.messages.build(),
                    "functions": self.functions.build(),
                }
            )

        async def _process(self, message: Message):
            print("Processing message.")
            self.messages.append(message)
            request = self._build()
            response = await process_request(request)
            self.messages.append(response)
            return response

        dct["id"] = generate_id(type(cls).__name__)
        dct["messages"] = Messages()
        dct["functions"] = Functions()
        dct["_build"] = _build
        dct["process"] = _process
        dct["_queues"] = Queues(other=cls, queues=["inbox", "parse", "outbox"])
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, *args, **kwargs):
        cls.__init__subclass__ = super().__init__(cls, name, bases)
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance
