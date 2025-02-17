from __future__ import annotations

import asyncio
import json

from inspect import Arguments, iscoroutine
from types import prepare_class
from typing import Any, Dict, Generic, TypeVar
from uuid import uuid5

import redis.asyncio as redis

from scint.api.models import Message
from scint.api.types import Trait
from scint.api.models import FunctionCall, Response
from scint.api.records import Record
from scint.api.aspects import intelligence


T = TypeVar("T")


class Intelligent(Trait):
    async def handle(self, obj: Any):
        self.update(obj)
        if isinstance(obj, Response):
            return self.callback(obj) if self.callback else self.output(obj)

        elif isinstance(obj, Message):
            res = await intelligence.parse_message(self)
            self.update(res)
            return await self.handle(res)

        elif isinstance(obj, FunctionCall):
            func = getattr(self.impl, obj.name)
            res = await func(**obj.args)
            self.update(res)
            final_res = await intelligence.parse_message(self)
            self.update(final_res)
            return await self.handle(final_res)


class Composable(Trait):
    def update(self, record: Record):
        match type(record).__name__:
            case "Message":
                self.persona.messages.append(record)
            case "Response":
                self.persona.messages.append(record)
            case "FunctionCall":
                self.persona.messages.append(record)
            case "FunctionResult":
                self.persona.messages.append(record)
            case _:
                return


class Constructable(Trait):
    def construct(name, args: Arguments) -> Generic[T]:
        from scint.api.aspects.memory import record_async, record_sync

        def decorate(self, ns: Dict[str, Any]):
            for k, v in ns.items():
                if callable(v) and not k.startswith("_"):
                    ns[k] = record_async(v) if iscoroutine(v) else record_sync(v)

        mcls, dct, kwds = prepare_class(name, args.types, {})
        dct["id"] = lambda: str(uuid5(dct, name))
        dct["name"] = name
        dct["methods"] = [
            v for k, v in dct.items() if not k.startswith("_") and callable(v)
        ]
        dct["__init__"] = lambda self, impl: self.impl
        dct["__slots__"] = ()
        new = mcls(name, args.types, dct, **kwds)
        return new()


class Subscribable(Trait):
    async def subscribe(self, *args, **kwargs):
        r = await redis.from_url(self.url)
        async with r.pubsub() as pubsub:
            if not pubsub.subscribed:
                await pubsub.subscribe(self.subscribe_channel)
            return await asyncio.create_task(self._reader(pubsub))

    async def _reader(self, pubsub):
        while True:
            data = await pubsub.get_message(ignore_subscribe_messages=True)
            if data is not None:
                message = Message(**json.loads(data["data"]))
                if self.callback:
                    return await self.callback(message)
                return message


class Publishable(Trait):
    async def publish(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            r = await redis.from_url(self.url)
            if self.subscribe:
                await r.publish(self.publish_channel, args[0].model_dump_json())
                return await self.subscribe()
            return await r.publish(self.publish_channel, args[0].model_dump_json())
        return self.__call__(*args, **kwargs)
