from __future__ import annotations

from typing import Any, List, Optional

from attrs import define, field
from meilisearch_python_sdk.models.search import Hybrid


@define
class Search:
    query = field(default=None)
    filter = field(type=Optional[str], default=None)
    vector = field(type=Optional[List[float]], default=None)
    limit = field(type=Optional[int], default=6)
    hybrid = field(
        type=Optional[Hybrid], default=Hybrid(semantic_ratio=0.9, embedder="default")
    )


@define
class SearchHits:
    hits: List[Any] = field(factory=list)
