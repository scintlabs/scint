from __future__ import annotations
from typing import List

from attrs import define, field

from .threads import Thread
from src.base.utils import timestamp, iso_to_epoch

SIMILARITY_THRESHOLD = 0.85


@define
class Attention:
    thread: Thread = field(default=None)
    last_n: int = field(default=4)
    cutoff_sec: int = 60 * 60 * 6

    async def build_focus(self):
        if not self.thread:
            return ""
        body = await self.thread.build(self.last_n)
        return "## Active Thread\n" + body

    async def build_recent(self, threads: List[Thread]):
        now = timestamp()
        recents = [
            t
            for t in self.threads
            if now - iso_to_epoch(t.metadata.events[-1]["created"]()) <= self.cutoff_sec
        ][:5]
        if not recents:
            return ""
        blocks = []
        for t in recents:
            last = t.events[-1]
            blocks.append(f"[{t.id}] {last.role}: {last.content}")
        return "## Recent Threads\n" + "\n".join(blocks)
