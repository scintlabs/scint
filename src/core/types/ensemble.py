from __future__ import annotations

import asyncio
import os
from typing import Dict, List

import kuzu
from attrs import define, field

from src.core.types.context import Context
from src.core.types.signals import Signal
from src.core.types.structure import Struct
from src.data.graph import ensure_schema
from src.data.indexes import Index


def ensembles(ensemble: str):
    db = kuzu.Database(os.path.join("src/data/graphs", ensemble))
    con = kuzu.Connection(db)
    return ensure_schema(con)


@define
class Ensemble:
    name: str
    structs: List[Struct] = field(factory=list)
    indexes: Dict[str, Index] = field(factory=dict)
    contexts: List[Context] = field(factory=list)

    async def handle(self, signal: Signal):
        async def sink(signal):
            self.input.append(signal)

        sink_task = asyncio.create_task(sink(signal))

        while True:
            if not self.input:
                done, pending = await asyncio.wait(
                    [asyncio.create_task(self._queue_event.wait()), sink_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )

                if sink_task in done and not self.input:
                    break

            while self.input:
                current_signal = self.input.popleft()
                async for res in self.parse(current_signal):
                    yield res

            while self.output:
                output_signal = self.output.popleft()
                async for res in self.parse(output_signal):
                    yield res

        if not sink_task.done():
            sink_task.cancel()
            try:
                await sink_task
            except asyncio.CancelledError:
                pass
