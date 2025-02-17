from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

from scint.lib.intelligence import generate_embedding
from scint.lib.observability import Observant
from scint.lib.schema.records import Record
from scint.lib.library import Library, Catalog
from scint.lib.threads import Thread, Threads
from scint.lib.struct import Struct
from scint.lib.traits import Trait, Traits
from scint.lib.util.typing import Constructor
from scint.lib.util.utils import cosine_similarity


EMBEDDING_THRESHOLD = 6
SIMILARITY_THRESHOLD = 0.8
SPLIT_MESSAGE_COUNT = 2


_contexts: Dict[str, Thread] = {}


class Contextual:
    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.name = name

    def __get__(self, instance: Optional[Any], owner: Type[Any]) -> Any:
        if instance is None:
            return self

        if instance.type != "Composer":
            if instance.id not in _contexts:
                _contexts[instance.id] = Thread()
            return _contexts[instance.id]

        return _contexts

    def __set__(self, instance: Any, value: Any) -> None:
        raise AttributeError("Context cannot be set directly")


class ContextConstructor(Constructor):
    Thread = ("Thread", (Thread,), {})
    Timeline = ("Threads", (Threads,), {})
    Record = ("Record", (Record,), {})
    Catalog = ("Catalog", (Catalog,), {})
    Library = ("Library", (Library,), {})


class Perspective(Trait):
    def current_metadata(self):
        self.keywords = [", ".join(m.keywords) for m in self.messages]
        content = ["".join(b.text for b in (m for m in self.messages))]
        self.embeddings.append(generate_embedding(content))

    def update_metadata(self):
        self.keywords = [", ".join(getattr(m, "keywords", [])) for m in self.messages]

        content = [
            "".join(getattr(b, "text", "") for b in getattr(m, "content", []))
            for m in self.messages
        ]
        new_embedding = generate_embedding(content)

        if self.embeddings:
            previous_embedding = self.embeddings[-1]
            similarity = cosine_similarity(previous_embedding, new_embedding)
            if similarity < SIMILARITY_THRESHOLD:
                self.split_thread()

        self.embeddings.append(new_embedding)


class Composing(Trait):
    def find_threads(self, thread: Thread) -> List[Thread]:
        related = []
        for context_id, existing_thread in _contexts.items():
            if existing_thread.id != thread.id:
                for embedding in thread.embeddings:
                    for existing_embedding in existing_thread.embeddings:
                        similarity = cosine_similarity(embedding, existing_embedding)
                        if similarity > SIMILARITY_THRESHOLD:
                            related.append(existing_thread)
                            break
        return related

    def split_thread(self, thread: Thread):
        new_context = ContextConstructor[self.name].new()
        new_context.prev = self
        self.next = new_context
        if self.thread:
            self.thread.register(new_context)

    def compose_thread(self, thread: Thread, record: Record = None):
        timeline = self.constructor.Timeline.new()
        timeline.current = thread

        if record:
            self.connection_manager.connect(thread.id, record.id, "referenced_records")

        related_threads = self.find_related_threads(thread)
        for related_thread in related_threads:
            self.connection_manager.connect(
                thread.id, related_thread.id, "semantic_connections"
            )

        return timeline

    def compose_view(self, thread_id: str, depth: int = 1) -> Dict:
        thread = _contexts[thread_id]
        view = {
            "thread": thread,
            "related_threads": [],
            "records": [],
            "semantic_connections": [],
        }

        record_ids = self.connection_manager.get_connections(
            thread_id, "referenced_records"
        )

        view["records"] = [self.get_record(rid) for rid in record_ids]

        if depth > 0:
            semantic_connections = self.connection_manager.get_connections(
                thread_id, "semantic_connections"
            )
            for connected_id in semantic_connections:
                connected_view = self.compose_view(connected_id, depth - 1)
                view["semantic_connections"].append(connected_view)

        return view


class Composer(Struct):
    traits: Traits = Traits(Perspective, Observant)
    context: Contextual = Contextual()
    constructor: Constructor = ContextConstructor
