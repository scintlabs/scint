from __future__ import annotations

import asyncio
from types import SimpleNamespace
from functools import partial
from typing import TypeAlias

from src.core.agents.dispatcher import Dispatcher
from src.model.records import Message, Envelope

Container: TypeAlias = SimpleNamespace
ns = partial(SimpleNamespace, _mutable=False)


async def bootstrap():
    dsp = Dispatcher()
    dsp.load()
    dsp.start()
    dsp.ref().tell(Envelope.create("user", Message("Hello, Scint!")))
    await asyncio.sleep(1)
