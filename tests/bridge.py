from __future__ import annotations

import asyncio
import json
from typing import Any

from attrs import define, field
from redis.asyncio import from_url
from src.model.records import Message


@define
class Bridge:
    redis_url: str = field(default=None)
    inbound: str = field(default=None)
    outbound: str = field(default=None)

    async def start(self):
        await super().start()
        self._redis = await from_url(self.redis_url, decode_responses=True)
        self._reader_task = asyncio.create_task(self._reader())

    async def stop(self):
        self._reader_task.cancel()
        await super().stop()

    async def on_receive(self, obj: Any):
        await self._redis.publish(self.outbound, json.dumps(obj.payload))

    async def _reader(self):
        async with self._redis.pubsub() as pub:
            await pub.subscribe(self.inbound)
            async for m in pub.listen():
                if m["type"] == "message":
                    payload = json.loads(m["data"])
                    self._broker.tell(payload["dest"], Message(**payload))


# @define
# class Bridge:
#     host: str = field(default=None)
#     queue: Deque = deque()

#     async def publish(self, obj):
#         r = await self.client.from_url(self.host)
#         await self.subscribe()
#         await r.publish("input", obj)

#     async def subscribe(self):
#         r = await self.client.from_url(self.host)
#         async with r.pubsub() as pubsub:
#             if not pubsub.subscribed:
#                 await pubsub.subscribe("output")
#             await asyncio.create_task(self._reader(pubsub))

#     async def _reader(self, pubsub):
#         while True:
#             message = await pubsub.get_message(ignore_subscribe_messages=True)
#             if message is not None:
#                 self.queue.append(message["data"].decode())
