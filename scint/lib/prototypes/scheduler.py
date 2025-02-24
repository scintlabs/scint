from __future__ import annotations
from __future__ import annotations

import asyncio
from typing import Callable, Dict, List, Set, Any
from threading import Lock
from redis.asyncio import Redis

from scint.lib.types import Struct, Trait
from scint.lib.schemas.signals import Event, Message
from scint.lib.types.model import Model
from scint.lib.util.utils import env

_observers: Dict[str, Set[Callable]] = {}
_observer_lock = Lock()


class Notification(Model):
    pass


class Publishing(Trait):
    async def publish(self, channel: str, message: Message):
        r = await Redis.from_url(env("REDIS_URL"))
        msg = message.model_dump_json()
        await r.publish(channel, msg)
        await self.subscribe(channel)


class Subscribing(Trait):
    async def subscribe(self, channel: str, callback: Callable):
        async def _reader(pubsub):
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    callback(message["schema"].decode())

        r = await Redis.from_url(env("REDIS_URL"))
        async with r.pubsub() as pubsub:
            if not pubsub.subscribed:
                await pubsub.subscribe(channel)
            await asyncio.create_task(_reader(pubsub))


class Observe(Trait):
    def subscribe(event_type: str, observer_fn: Callable) -> bool: ...


class Observable(Trait):
    def subscribe(event_type: str, observer_fn: Callable) -> bool:
        if not callable(observer_fn):
            return False

        with _observer_lock:
            if event_type not in _observers:
                _observers[event_type] = set()

            _observers[event_type].add(observer_fn)
            return True

    def unsubscribe(event_type: str, observer_fn: Callable) -> bool:
        with _observer_lock:
            if event_type not in _observers:
                return False

            if observer_fn in _observers[event_type]:
                _observers[event_type].remove(observer_fn)

                if not _observers[event_type]:
                    del _observers[event_type]
                return True

            return False

    def notify(event_type: str, *args, **kwargs) -> None:
        with _observer_lock:
            if event_type not in _observers:
                return

            observers = list(_observers[event_type])

        for observer in observers:
            try:
                observer(*args, **kwargs)
            except Exception:
                pass

    def clear_observers() -> None:
        with _observer_lock:
            _observers.clear()


class Notify(Trait):
    def add_entry(self, obj: Any):
        self.entries[obj.id] = Notification(object_id=obj.id, object_ref=obj)

    def get_entry(self, obj_id: str) -> Notification:
        return self.directory[obj_id]

    def remove_entry(self, obj_id: str) -> None:
        if obj_id not in self.entries:
            raise KeyError(f"Entry {obj_id} not found")
        del self.entries[obj_id]

    def add_event(self, event: Event):
        self.events[event.event_type].append(event)


class Notifier(Struct):
    traits: List[Trait] = [Notify, Observable]
    entries: Dict[str, Notification] = {}
    events: Dict[str, List[Event]] = {}
