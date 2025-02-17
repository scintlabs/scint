from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, Any, TypeVar
from datetime import datetime as dt
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class Record(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created: str = Field(default_factory=lambda: dt.now().isoformat())
    modified: str = Field(default_factory=lambda: dt.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)
    model_config = ConfigDict(arbitrary_types_allowed=True)


class ContentType(Enum):
    TextContent = "TextContent"
    CodeContent = "CodeContent"
    ImageContent = "ImageContent"
    AudioContent = "AudioContent"
    VideoContent = "VideoContent"
    StructuredContent = "StructuredContent"
    BinaryContent = "BinaryContent"


class CatalogType(Enum):
    FileSystem = "FileSystem"
    DOMTree = "DOMTree"
    Database = "Database"
    Graph = "Graph"
    Collection = "Collection"


class Content(Record):
    type: ContentType
    content: str
    annotation: str
    embedding: Optional[List[float]] = None
    references: List[str] = Field(default_factory=list)


class ImageContent(Content):
    type: ContentType = ContentType.ImageContent
    data: str
    mime_type: str
    dimensions: Optional[tuple[int, int]] = None


class DataNode(Record):
    name: str
    path: str
    content: Optional[Content] = None
    children: List[DataNode] = Field(default_factory=list)
    parent_id: Optional[str] = None
    relationships: Dict[str, List[str]] = Field(default_factory=dict)

    def add_child(self, node: DataNode):
        node.parent_id = self.id
        self.children.append(node)

    def find_by_path(self, path: str) -> Optional[DataNode]:
        parts = path.split("/")
        current = self
        for part in parts:
            found = False
            for child in current.children:
                if child.name == part:
                    current = child
                    found = True
                    break
            if not found:
                return None
        return current


class Index(Record):
    name: str
    key: str
    sortables: List[str]
    filterables: List[str]
    searchables: List[str]
    embedding_config: Optional[Dict[str, Any]] = None
