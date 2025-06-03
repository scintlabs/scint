from __future__ import annotations

import json
from typing import Callable, Dict

from attrs import define, field

from src.svc.indexes import Indexes


@define
class Library:
    indexes: Indexes = field(default=None)
    outlines: Dict[str, Callable] = field(factory=dict)
    directions: Dict[str, Callable] = field(factory=dict)
    _loaded: bool = field(default=False)

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
