from __future__ import annotations

import json
from typing import Dict

from attrs import define

from src.base.actor import Address


@define
class Directory:
    _agents: Dict[str, Address]
    _resources: Dict[str, Address]
    _services: Dict[str, Address]

    async def load(self):
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
                    records = [
                        {"id": t.get("_sig"), **t.get("schema", {})} for t in data
                    ]
                    await idx.update_documents(records)
