from __future__ import annotations

from typing import List, Callable

from attrs import define, field

SIMILARITY_THRESHOLD = 0.85


@define
class Similarity:
    embed: List[float] = field(factory=list)
    top_k: int = 6
    search: Callable = field(default=None, repr=False)

    async def build(self):
        if not self.embed or not self.search:
            return ""
        hits = await self.search(self.embed, self.top_k)
        results = [h.get("content", "") for h in hits.hits]
        if not results:
            return ""
        return "## Semantic Search\n" + "\n".join(results)
