from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Document:
    id: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime


@dataclass
class Document:
    id: str
    content: str
    embeddings: Optional[List[float]] = None
    labels: Optional[List[str]] = None


@dataclass
class MaterializedDocument:
    id: str
    content: str
    embeddings: Optional[List[float]] = None
    labels: List[str] = field(default_factory=list)
    processing_state: ProcessingState = field(default_factory=ProcessingState.PENDING)
    last_updated: datetime = field(default_factory=datetime.utcnow)
