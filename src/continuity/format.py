from __future__ import annotations

from typing import Sequence

from src.continuity.attention import Attention
from src.continuity.preferences import Preferences
from src.continuity.similarity import Similarity
from src.continuity.status import Status
from src.continuity.threads import Thread


SEPARATOR = "\n\n---\n\n"


async def format_context(self, thread: Thread):
    preferences = Preferences()
    attention = Attention(thread=thread)
    similarity = Similarity(embed=thread.embed, search=self.search)
    status = Status()
    context = [preferences, attention, similarity, status]
    return SEPARATOR.join(filter(None, context))


def _join(parts: Sequence[str]) -> str:
    return "\n\n".join(p for p in parts if p)
