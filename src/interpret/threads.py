from __future__ import annotations

from enum import Enum
from typing import Callable, List, Optional, Type

from attrs import define, field

from src.base.records import Content, EncodedContent, Metadata
from src.base.utils import timestamp


class ThreadEvent(Enum):
    Created = {"created": lambda: timestamp()}
    Staled = {"staled": lambda: timestamp()}
    Encoded = {"encoded": lambda: timestamp()}
    Purged = {"purged": lambda: timestamp()}

    def __init__(self, event):
        self.event = event

    def __call__(self, content: str = None):
        if content is not None:
            self.event["content"] = content
        return self.event


@define
class Thread:
    metadata: Metadata | None = None
    content: List[Content] = field(factory=list)
    prev: Optional[Thread] = None
    next: Optional[Thread] = None

    def _record(self, event: ThreadEvent, msg: str | None = None):
        self.metadata.events.append(event(msg) if msg else event())

    async def update(self, content: Content, *, embed: List[float] | None = None):
        self.content.append(content)
        if embed is not None:
            self.metadata.embedding = embed

    async def build(self, k: int = 6):
        head = self.metadata.description or ""
        body = "\n".join(self.render(m) for m in self.content[-k:])
        return f"{head}\n{body}"

    def render(self, c: Content):
        return str(c)

    _NEXT: Type[Thread] | None = None
    _EVENT_AFTER: ThreadEvent | None = None

    def _transform_content(self):
        return self.content

    def transition(self):
        if self._NEXT is None or self._EVENT_AFTER is None:
            raise NotImplementedError("Subclass didn’t set _NEXT/_EVENT_AFTER")
        nxt = self._NEXT(
            metadata=self.metadata,
            prev=self.prev,
            next=self.next,
            content=self._transform_content(),
        )
        nxt._record(self._EVENT_AFTER)
        return nxt


@define
class ActiveThread(Thread):
    _NEXT = None
    _EVENT_AFTER = ThreadEvent.Staled


@define
class StaleThread(Thread):
    _NEXT = None
    _EVENT_AFTER = ThreadEvent.Encoded

    def _transform_content(self) -> List[EncodedContent]:
        return [EncodedContent() for _ in self.content]


@define
class EncodedThread(Thread):
    _NEXT = None
    _EVENT_AFTER = ThreadEvent.Purged

    def transition(self):
        nxt = super().transition()
        nxt.metadata.events[-1]["content"] = "Content purged"
        return nxt


@define
class PurgedThread(Thread):
    _NEXT = None
    _EVENT_AFTER = None


@define
class Threads:
    head: Optional[Thread] = None
    tail: Optional[Thread] = None
    maxlen: int = 0
    stale_threshold: int = 10
    encoded_threshold: int = 20
    should_purge: Callable[[StaleThread], bool] = lambda self, t: False
    counts: dict[str, int] = field(
        factory=lambda: {
            n: 0 for n in (ActiveThread, StaleThread, EncodedThread, PurgedThread)
        }
    )

    def append(self, *, metadata: Metadata = None, left: bool = False):
        node = ActiveThread(metadata or Metadata())
        node._record(ThreadEvent.Created)

        if self.head is None:
            self.head = self.tail = node
        elif left:
            node.next, self.head.prev = self.head, node
            self.head = node
        else:
            node.prev, self.tail.next = self.tail, node
            self.tail = node

        self._bump(ActiveThread, +1)
        self._maybe_rollover()
        return node

    def pop(self, *, left: bool = False):
        if self.head is None:
            raise IndexError("pop from empty Threads")
        node = self.head if left else self.tail
        self._detach(node)
        self._bump(type(node).__name__, -1)
        return node

    def walk(self, *types):
        cur = self.head
        while cur:
            if not types or isinstance(cur, types):
                yield cur
            cur = cur.next

    def _bump(self, name: str, d: int):
        self.counts[name] += d

    def _detach(self, n: Thread):
        if n.prev:
            n.prev.next = n.next
        else:
            self.head = n.next
        if n.next:
            n.next.prev = n.prev
        else:
            self.tail = n.prev
        n.prev = n.next = None

    def _maybe_rollover(self):
        self._rollover(ActiveThread, self.maxlen, self._to_stale)
        self._rollover(StaleThread, self.stale_threshold, self._advance_stale)

    def _rollover(self, kind: str, limit: int, advance: Callable[[Thread], Thread]):
        while self.counts[kind] > limit:
            node = self._oldest(kind)
            if node is None:
                break
            nxt = advance(node)
            self._replace(node, nxt)

    def _to_stale(self, node: ActiveThread):
        nxt = StaleThread(
            metadata=node.metadata, prev=node.prev, next=node.next, content=node.content
        )
        nxt._record(ThreadEvent.Staled)
        self._shift_counts(ActiveThread, StaleThread)
        return nxt

    def _advance_stale(self, node: StaleThread):
        purge = self.should_purge(node)
        nxt = node.transition(purge=purge)
        self._shift_counts(StaleThread, type(nxt).__name__)
        if purge:
            return nxt

        self._replace(node, nxt)
        self._rollover(EncodedThread, self.encoded_threshold, self._purge_encoded)
        return nxt

    def _purge_encoded(self, node: EncodedThread) -> PurgedThread:
        nxt = PurgedThread(metadata=node.metadata, prev=node.prev, next=node.next)
        nxt._record(ThreadEvent.Purged, "Content purged")
        self._shift_counts(EncodedThread, PurgedThread)
        return nxt

    def _shift_counts(self, frm: str, to: str):
        self.counts[frm] -= 1
        self.counts[to] += 1

    def _oldest(self, kind: str):
        cls = globals()[kind]
        cur = self.head
        while cur and not isinstance(cur, cls):
            cur = cur.next
        return cur

    def _replace(self, old: Thread, new: Thread):
        if old.prev:
            old.prev.next = new
        else:
            self.head = new
        if old.next:
            old.next.prev = new
        else:
            self.tail = new
        new.prev, new.next = old.prev, old.next
        old.prev = old.next = None
