from __future__ import annotations

import asyncio
from enum import Enum, auto
from typing import Any, List, Optional

from scint.lib.prototypes.classifier import Classifier
from scint.lib.prototypes.notifier import Notifier
from scint.lib.schemas.signals import Signal
from scint.lib.types import Struct, Trait


class Route(Enum):
    Classifiers = auto()
    Composers = auto()
    Interfaces = auto()
    Notifiers = auto()
    Parsers = auto()
    Processors = auto()
    Services = auto()


class Request(Signal):
    data: Any
    metadata: Optional[Any] = None
    route: Route = Route


class Switching(Trait):
    async def request(self, req: Request):
        try:
            if req.route:
                return await self.route_request(req)
            return await self.classifier.request(req)
        except asyncio.CancelledError:
            pass

    async def classify_request(self, req: Request):
        res = await self.classifier.classify(req)
        return await self.route_request(res)

    async def route_request(self, req: Request):
        async def sink():
            while True:
                try:
                    match req.route:
                        case Route.Compose:
                            await self.notifier.notify(req)
                except asyncio.CancelledError:
                    pass

        sink_task = asyncio.create_task(sink())

        while not sink_task.done():
            while self._requests.empty() and not sink_task.done():
                await asyncio.sleep(0.1)
            try:
                message = await self.subscribe()
                if message:
                    await self.publish(message)
                routable = await self._requests.get()
                if routable:
                    await self.handle_route(routable)
            except asyncio.CancelledError:
                pass

        sink_task.cancel()

        try:
            await sink_task
        except asyncio.CancelledError:
            pass


class Switch(Struct):
    traits: List[Trait] = [Switching]
    requests: List[Request] = []
    classifier = Classifier()
    notifier = Notifier()
