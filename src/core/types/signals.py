from __future__ import annotations

from typing import Any, Dict, List, Optional, TypeAlias, Union

from attrs import field
from meilisearch_python_sdk.models.search import Hybrid

from src.core.util.llms import embedding
from src.core.types.identity import signal


@signal
class Input:
    content: Content = field(default=None)
    embedding: List[float] = field(factory=list)

    def __attrs_post_init__(self):
        if isinstance(self.content, str) and len(self.content) > 50:
            self.embedding = embedding(self.content)


@signal
class Output:
    content: List[str]
    annotation: str
    predictions: List[str]
    keywords: List[str]


@signal
class ToolCall:
    call_id: str = field(default=None)
    tool_name: str = field(factory=str)
    arguments: Dict[str, Any] = field(factory=dict)

    @classmethod
    def create(cls, call: Any):
        return cls(id=call.call_id, name=call.name, arguments=call.arguments)


@signal
class ToolResult:
    call_id: str = field(default=None)
    tool_name: str = field(factory=str)
    content: str = field(factory=str)


@signal
class Query:
    index: str = field()
    content: str = field()
    limit: int = field(default=4)
    filter: Optional[str] = field(default=None)
    hybrid: Hybrid = Hybrid(semantic_ratio=0.9, embedder="default")


Content: TypeAlias = Union[str, Dict[str, Any]]
Signal: TypeAlias = Union[Input, Output, ToolCall, ToolResult, Query]
