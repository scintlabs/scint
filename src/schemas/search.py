from __future__ import annotations

from typing import Optional, List, Dict

from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.search import Hybrid

from src.types.base import Model, Signal
from src.types.service import Provider
from src.types.struct import Struct
from src.types.traits import Trait
from src.util.utils import env, generate_doc_id


class Query(Signal):
    index_name: str
    input: str
    category: Optional[str] = None
    limit: int = 4


class Document(Model): ...


search = Provider(
    name="Meilisearch",
    client=AsyncClient,
    settings={"url": "localhost", "key": env("MEILISEARCH_API_KEY")},
)


class Documenting(Trait):
    async def update_docs(self, index_name: str, docs: List[Dict]):
        index = self.client.index(index_name)
        updated_docs = [{"id": generate_doc_id(doc), **doc} for doc in docs]
        return await index.update_documents(updated_docs)

    async def delete_docs(self, index_name: str, filter: str):
        index = self.client.index(index_name)
        return await index.delete_documents_by_filter(filter)

    async def delete_all_docs(self, index_name: str):
        index = self.client.index(index_name)
        return await index.delete_all_documents()


class Searching(Trait):
    async def search(self, query: Query):
        index = self.client.index(query.index_name)
        return await index.search(
            query.input,
            hybrid=Hybrid(semantic_ratio=0.9, embedder="default"),
            limit=query.limit,
            filter=f"categories = {query.category}" if query.category else None,
        ).hits


class Indexing(Trait):
    async def add_index(self, index_name: str):
        return await self.client.create_index(index_name, "id")

    async def load_indexes(self):
        for index_name, docs in self.indexes.items():
            await self.update_docs(index_name, docs)

    async def update_index(self, index_name: str, attr: List[str]):
        index = self.client.index(index_name)
        return await index.update_filterable_attributes(attr)

    async def delete_index(self, index_name: str):
        index = self.client.index(index_name)
        return await index.delete()


class Indexer(Struct):
    traits = (Indexing,)
    indexes: Dict[str, List[Dict]]


# def update(self, signal: Signal):
#         sig = type(signal).__name__
#         match sig:
#             case "Message":
#                 self.messages.append(signal)
#             case "Event":
#                 self.events.append(signal)
#             case "Process":
#                 self.processes.append(signal)
#             case "Task":
#                 self.tasks.append(signal)
#             case "Goal":
#                 pass
#             case _:
#                 return

#     def pruned_messages(self, max_tokens: int = 1000):
#         pruned = []
#         cumulative_tokens = 0
#         for msg in self.messages:
#             tokens = msg.content.split()
#             token_count = len(tokens)
#             if cumulative_tokens + token_count > max_tokens:
#                 if msg.annotation:
#                     pruned.append(msg.annotation)
#                 else:
#                     remaining = max_tokens - cumulative_tokens
#                     pruned.append(" ".join(tokens[:remaining]))
#             else:
#                 pruned.append(msg.content)
#             cumulative_tokens += token_count
#         return pruned

#     def relevant_messages(self, preDiction: List[str], threshold: int = 1):
#         scored_messages = []
#         for msg in self.messages:
#             score = 0
#             content_lower = msg.content.lower() if msg.content else ""
#             annotation_lower = msg.annotation.lower() if msg.annotation else ""
#             for keyword in preDiction:
#                 keyword_lower = keyword.lower()
#                 if keyword_lower in content_lower:
#                     score += 1
#                 if keyword_lower in annotation_lower:
#                     score += 1
#             if score >= threshold:
#                 scored_messages.append((score, msg))
#         scored_messages.sort(key=lambda x: x[0], reverse=True)
#         return [msg for score, msg in scored_messages]

#     @property
#     def created(self):
#         timestamps = []
#         timestamps += [
#             dt.fromisoformat(msg.created) for msg in self.thread.messages if msg.created
#         ]
#         timestamps += [
#             dt.fromisoformat(evt.created) for evt in self.thread.events if evt.created
#         ]
#         return min(timestamps).isoformat() if timestamps else None

#     @property
#     def modified(self):
#         timestamps = []
#         timestamps += [
#             dt.fromisoformat(msg.created) for msg in self.thread.messages if msg.created
#         ]
#         timestamps += [
#             dt.fromisoformat(evt.created) for evt in self.thread.events if evt.created
#         ]
#         return max(timestamps).isoformat() if timestamps else None

#     @property
#     def embeddings(self):
#         total_embedding = None
#         total_weight = 0.0
#         for msg in self.messages:
#             if msg.embedding:
#                 weight = len(msg.content.split())
#                 total_weight += weight
#                 embedding_array = np.array(msg.embedding, dtype=float)
#                 if total_embedding is None:
#                     total_embedding = weight * embedding_array
#                 else:
#                     total_embedding += weight * embedding_array
#         if total_embedding is not None and total_weight > 0:
#             avg_embedding = total_embedding / total_weight
#             return avg_embedding.tolist()
#         return None


# def parse_created(created_str: str) -> dt:
#     return dt.fromisoformat(created_str)


# def sort_signals_by_time(signals: List[Signal]) -> List[Signal]:
#     return sorted(signals, key=lambda signal: parse_created(signal.created))


# def next_node(self) -> Optional[SemanticState]:
#         return self.next

#     def prev_node(self) -> Optional[SemanticState]:
#         return self.prev

#     def merge_with_next(self) -> None:
#         if not self.next:
#             return
#         self.thread.messages += self.next.thread.messages
#         self.thread.events += self.next.thread.events
#         self.next = self.next.next
#         if self.next:
#             self.next.prev = self

#     def get_context(self, max_tokens: int = 1000) -> str:
#         context = []
#         tokens_so_far = 0
#         for msg in self.thread.messages:
#             tokens = msg.content.split()
#             if tokens_so_far + len(tokens) > max_tokens:
#                 context.append(
#                     msg.annotation
#                     if msg.annotation
#                     else " ".join(tokens[: max_tokens - tokens_so_far])
#                 )
#                 break
#             else:
#                 context.append(msg.content)
#                 tokens_so_far += len(tokens)
#         return "\n".join(context)

#     def remove(self):
#         if self.prev:
#             self.prev.next = self.next
#         if self.next:
#             self.next.prev = self.prev
#         self.prev = None
#         self.next = None
