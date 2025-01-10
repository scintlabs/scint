from __future__ import annotations

from dataclasses import field
from typing import Any, List

from meilisearch_python_sdk.models.search import Hybrid

from ..core.agents import Agentic
from ..core.types import BaseType, MemoryType, Struct
from ..models import Event, Signal, File, Message
from ..util.utils import cosine_similarity


class Thread(Struct):
    signals: List[Signal] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
    files: List[File] = field(default_factory=list)


class Threads(metaclass=MemoryType):
    def __init__(self): ...


class Context(metaclass=MemoryType):
    def __init__(self):
        self.threads = Threads()

    def update(self, data: Any):
        if isinstance(data, Message):
            self.messages.append(data)

    @property
    def model(self):
        return {"messages": [m.model for m in self.messages]}


class Composer(Agentic, metaclass=BaseType):
    def __init__(self):
        self.threads = Threads()

    async def compose(self, message: Message):
        context = await self.get_context(message)
        self.contexts.append(context)
        return await context.interface.input(context)

    async def get_context(self, message):
        if len(self.contexts) > 0:
            max_similarity = 0.0
            selected_context = None

            for c in self.contexts:
                for e in c.embeddings:
                    sim = cosine_similarity(message.embedding, e)
                    if sim > max_similarity:
                        max_similarity = sim
                        selected_context = c

            if selected_context and max_similarity >= 0.85:
                self.contexts.append(selected_context)
                return selected_context
        return await self.create_context(message)

    async def create_context(self, message):
        try:
            context = Context()
            return context
        except Exception as e:
            raise ValueError(f"Failed to load interface: {str(e)}")

    async def classify_context(self, context, message):
        classification = await self.classify(message)
        description = classification.description
        context.description = description
        interface = self.interfaces.get_interface(classification.interface)
        context.interface = interface

    async def augment_context(self, context: Context, message: Message):
        async def _search(category: str, query: str):
            res = await self.search.results(category, query)
            for obj in res:
                obj.pop("id")
            return res

        query = "".join([b.data for b in message.content])
        context.interface.prompts = await _search("prompts", query)
        context.interface.functions = await _search("functions", message)
        user = await _search("user", message)
        knowledge = await _search("knowledge", message)
        messages = await _search("messages", message)
        context.messages = [*user, *knowledge, *messages]
        return context

    async def search_context(self, client, index_name, query, category=None, limit=4):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        category_filter = f"categories = {category}" if category else None
        index = client.index(index_name)
        res = await index.search(
            query, hybrid=hybrid, limit=limit, filter=category_filter
        )
        return res.hits
