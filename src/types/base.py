from __future__ import annotations

from uuid import uuid4
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime as dt, timezone as tz

from pydantic import BaseModel, ConfigDict, Field


class BlockType(str, Enum):
    TextBlock = "TextBlock"
    CodeBlock = "CodeBlock"
    ImageBlock = "ImageBlock"
    AudioBlock = "AudioBlock"
    BinaryBlock = "BinaryBlock"


class SignalType(str, Enum):
    Event = "Event"
    Message = "Message"
    Action = "Action"


class Block(BaseModel):
    content: str
    type: BlockType = BlockType.TextBlock
    id: str = Field(default_factory=lambda: str(uuid4()))

    @property
    def timestamp(self):
        return str(dt.now(tz.utc).isoformat())


class Signal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    @property
    def timestamp(self):
        return str(dt.now(tz.utc).isoformat())


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    created: str = Field(default_factory=lambda: str(dt.now(tz.utc).isoformat()))
    modified: str = Field(default_factory=lambda: dt.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def timestamp(self):
        return str(dt.now(tz.utc).isoformat())


class Index(BaseModel):
    category: Optional[str] = None
