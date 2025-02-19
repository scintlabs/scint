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


class BlockType(Enum):
    TextContent = "TextContent"
    CodeContent = "CodeContent"
    ImageContent = "ImageContent"
    AudioContent = "AudioContent"
    VideoContent = "VideoContent"
    StructuredContent = "StructuredContent"
    BinaryContent = "BinaryContent"


class ImageBlock(Record):
    type: BlockType = BlockType.ImageContent
    data: str
    mime_type: str
    dimensions: Optional[tuple[int, int]] = None


class Block(Record):
    type: BlockType = BlockType.TextContent
    content: str
    annotation: str


class Goal(Record): ...


class Index(Record):
    name: str
    key: str
    sortables: List[str]
    filterables: List[str]
    searchables: List[str]
    embedding_config: Optional[Dict[str, Any]] = None
