from __future__ import annotations

import json
from typing import Callable, Dict

from attrs import define, field

from src.runtime.actor import Actor
from src.services.indexes import Indexes


@define
class Library(Actor):
    _outlines: Dict[str, Callable] = field(factory=dict)
    _directions: Dict[str, Callable] = field(factory=dict)
    _instructions: Dict[str, Callable] = field(factory=dict)
    _indexes: Indexes = Indexes()

    async def load(self):
        if self._loaded:
            return
        async with self._lock:
            await self._load_modules()
            self._loaded = True

    async def _load_modules(self):
        await self._indexes.load_indexes()
        for cfg in ("directions", "outlines", "instructions", "tools"):
            with open(f"config/{cfg}.json", "r") as f:
                data = json.loads(f.read())
                setattr(self, cfg, data)
                if cfg == "tools":
                    idx = await self._indexes.get_index("tools")
                    records = [{"id": t.get("_sig"), **t.get("schema", {})} for t in data]
                    await idx.update_documents(records)
