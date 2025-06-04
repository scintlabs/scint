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
        for cfg in ("directions", "outlines"):
            with open(f"config/{cfg}.json", "r") as f:
                setattr(self, cfg, json.loads(f.read()))
