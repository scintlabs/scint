from __future__ import annotations

from typing import Any, Dict, List, Optional, TypeAlias, Union, TypeVar

from attrs import define, field
from meilisearch_python_sdk.models.search import Hybrid

T = TypeVar("T")
Content: TypeAlias = Union[str, List[str], Dict[str, Any]]


@define
class Search:
    query = field(default=None)
    filter = field(type=Optional[str], default=None)
    hybrid = field(
        type=Optional[Hybrid], default=Hybrid(semantic_ratio=0.9, embedder="default")
    )
    vector = field(type=Optional[List[float]], default=None)
    limit = field(type=Optional[int], default=6)


@define
class SearchHits:
    hits: List[Any] = field(factory=list)
