from __future__ import annotations

from attrs import define

from src.base.utils import timestamp


@define
class Status:
    async def build(self):
        parts = []
        parts.append("## System Info")
        parts.append(f"{timestamp()}")
        return "\n\n".join(parts)
