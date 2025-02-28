from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from src.types.base import Block, Signal


class SystemMessage(Signal):
    content: str
    entities: Optional[List[str]] = []
    keywords: Optional[List[str]] = []

    @property
    def model(self):
        return {
            "role": "system",
            "content": self.content,
        }

    @classmethod
    def from_docstring(cls, docstring: str):
        lines = docstring.strip().split("\n")
        name = lines[0].strip()
        content_start = 3
        content = "\n".join(lines[content_start:]).strip()
        return cls(name=name, blocks=[Block(content=content)])


class ContextMessage(Signal):
    content: str
    entities: Optional[List[str]]
    key: str

    @property
    def model(self):
        return {"role": "user", "content": f"{self.timestamp}\n{self.content}"}


class UserMessage(Signal):
    content: str
    embedding: Optional[List[float]] = None

    @property
    def model(self):
        return {"role": "user", "content": f"{self.timestamp}\n{self.content}"}


class Message(Signal):
    blocks: List[Block]
    keywords: List[str]
    prediction: List[str]
    annotation: str

    @property
    def model(self):
        return {
            "role": "assistant",
            "content": f"{self.timestamp}\n".join(b.content for b in self.blocks),
        }


class ToolCall(Signal):
    tool_call_id: str
    name: str
    arguments: Dict[str, Any]

    @property
    def model(self):
        return {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": self.tool_call_id,
                    "type": "function",
                    "function": {
                        "name": self.name,
                        "arguments": json.dumps(self.arguments),
                    },
                }
            ],
        }


class ToolResult(Signal):
    tool_call_id: Optional[str] = None
    content: Optional[str] = None

    @property
    def model(self):
        return {
            "role": "tool",
            "tool_call_id": self.tool_call_id,
            "content": f"{self.timestamp}\n{self.content}",
        }
