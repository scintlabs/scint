from __future__ import annotations

from enum import Enum
from uuid import uuid4
from datetime import datetime as dt, timezone as tz
from typing import Deque, List, Optional

import numpy as np
from pydantic import BaseModel, Field, ConfigDict

from scint.lib.common.struct import Struct
from scint.lib.common.traits import Trait


def parse_created(created_str: str) -> dt:
    return dt.fromisoformat(created_str)


def sort_signals_by_time(signals: List[Signal]) -> List[Signal]:
    return sorted(signals, key=lambda signal: parse_created(signal.created))


class Signal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(uuid4()))
    created: str = Field(default_factory=lambda: dt.now(tz.utc).isoformat())


class EventType(Enum):
    ToolCall = "ToolCall"
    ToolResult = "ToolResult"
    Query = "Query"


class Event(Signal):
    type: EventType
    content: str


class ResultType(Enum):
    FunctionCall = "FunctionCall"
    ProcessCall = "ProcessCall"
    SearchQuery = "SearchQuery"


class Result(Signal):
    type: ResultType
    content: Result

    @property
    def model(self):
        {"role": "tool", "tool_call_id": self.call_id, "content": self.result}


class ProcessCall(Signal):
    call_id: str
    content: List[Result]

    @property
    def model(self):
        return {
            "role": "tool",
            "tool_call_id": self.call_id,
            "results": [r.content for r in self.content],
        }


class FunctionCall(Signal):
    call_id: str
    result: Result

    @property
    def model(self):
        return {
            "role": "tool",
            "tool_call_id": self.call_id,
            "content": self.result.content,
        }


class ContentType(Enum):
    TextContent = "TextContent"
    CodeContent = "CodeContent"
    ImageContent = "ImageContent"


class Content(Signal):
    type: ContentType
    content: str
    annotation: str


class Response(Signal):
    content: List[Content]
    entities: Optional[List[str]]
    keywords: List[str]
    prediction: List[str]


class Message(Signal):
    content: str
    embedding: Optional[List[float]] = None


class Thread(Struct):
    id: str
    goal: str
    tasks: List[Deque] = []
    processes: List[Deque] = []
    events: List[Event] = []
    messages: List[Message] = []

    def pruned_messages(self, max_tokens: int = 1000):
        pruned = []
        cumulative_tokens = 0
        for msg in self.messages:
            tokens = msg.content.split()
            token_count = len(tokens)
            if cumulative_tokens + token_count > max_tokens:
                if msg.annotation:
                    pruned.append(msg.annotation)
                else:
                    remaining = max_tokens - cumulative_tokens
                    pruned.append(" ".join(tokens[:remaining]))
            else:
                pruned.append(msg.content)
            cumulative_tokens += token_count
        return pruned

    def relevant_messages(self, prediction: List[str], threshold: int = 1):
        scored_messages = []
        for msg in self.messages:
            score = 0
            content_lower = msg.content.lower() if msg.content else ""
            annotation_lower = msg.annotation.lower() if msg.annotation else ""
            for keyword in prediction:
                keyword_lower = keyword.lower()
                if keyword_lower in content_lower:
                    score += 1
                if keyword_lower in annotation_lower:
                    score += 1
            if score >= threshold:
                scored_messages.append((score, msg))
        scored_messages.sort(key=lambda x: x[0], reverse=True)
        return [msg for score, msg in scored_messages]

    @property
    def created(self):
        timestamps = []
        timestamps += [
            dt.fromisoformat(msg.created) for msg in self.thread.messages if msg.created
        ]
        timestamps += [
            dt.fromisoformat(evt.created) for evt in self.thread.events if evt.created
        ]
        return min(timestamps).isoformat() if timestamps else None

    @property
    def modified(self):
        timestamps = []
        timestamps += [
            dt.fromisoformat(msg.created) for msg in self.thread.messages if msg.created
        ]
        timestamps += [
            dt.fromisoformat(evt.created) for evt in self.thread.events if evt.created
        ]
        return max(timestamps).isoformat() if timestamps else None

    @property
    def embeddings(self):
        total_embedding = None
        total_weight = 0.0
        for msg in self.messages:
            if msg.embedding:
                weight = len(msg.content.split())
                total_weight += weight
                embedding_array = np.array(msg.embedding, dtype=float)
                if total_embedding is None:
                    total_embedding = weight * embedding_array
                else:
                    total_embedding += weight * embedding_array
        if total_embedding is not None and total_weight > 0:
            avg_embedding = total_embedding / total_weight
            return avg_embedding.tolist()
        return None


class Timeline(Struct):
    current: Thread
    prev: Thread
    next: Thread

    def next_node(self) -> Optional[Timeline]:
        return self.next

    def prev_node(self) -> Optional[Timeline]:
        return self.prev

    def remove(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev
        self.prev = None
        self.next = None

    def merge_with_next(self) -> None:
        if not self.next:
            return
        self.thread.messages += self.next.thread.messages
        self.thread.events += self.next.thread.events
        self.next = self.next.next
        if self.next:
            self.next.prev = self

    def get_context(self, max_tokens: int = 1000) -> str:
        context = []
        tokens_so_far = 0
        for msg in self.thread.messages:
            tokens = msg.content.split()
            if tokens_so_far + len(tokens) > max_tokens:
                context.append(
                    msg.annotation
                    if msg.annotation
                    else " ".join(tokens[: max_tokens - tokens_so_far])
                )
                break
            else:
                context.append(msg.content)
                tokens_so_far += len(tokens)
        return "\n".join(context)


class Composable(Trait):
    pass


class Oracular(Trait):
    pass


Message = Message | Response | FunctionCall | ProcessCall | Result
