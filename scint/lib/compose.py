from __future__ import annotations

from typing import Dict, List

from scint.lib.intelligence import generate_embedding
from scint.lib.observability import Observant
from scint.lib.schema.records import Record
from scint.lib.context import ContextProvider, _context
from scint.lib.types.traits import Traits, Trait
from scint.lib.types.agent import Agent
from scint.lib.util.utils import cosine_similarity


EMBEDDING_THRESHOLD = 6
SIMILARITY_THRESHOLD = 0.8
SPLIT_MESSAGE_COUNT = 2


class Perceive(Trait):
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


class Compose(Trait):
    def find_threads(self, thread: ContextProvider) -> List[ContextProvider]:
        related = []
        for context_id, existing_thread in _context.items():
            if existing_thread.id != thread.id:
                for embedding in thread.embeddings:
                    for existing_embedding in existing_thread.embeddings:
                        similarity = cosine_similarity(embedding, existing_embedding)
                        if similarity > SIMILARITY_THRESHOLD:
                            related.append(existing_thread)
                            break
        return related

    def compose_thread(self, thread: ContextProvider, record: Record = None):
        timeline = self.constructor.Temporal.new()
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
        thread = _context[thread_id]
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


class Composer(Agent):
    traits: Traits = Traits(Compose, Perceive, Observant)
    context: ContextProvider = ContextProvider()
