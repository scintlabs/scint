from __future__ import annotations


from enum import Enum
import re
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, ConfigDict, Field

from scint.lib.schema.signals import Block


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Intention(Model):
    description: str
    keywords: List[str]
    content: Block

    @property
    def model(self):
        return {"role": "system", "content": self.content.content}


"""
Name of Prompt
This is the description line. A single line.

This is the content. Everything after the description line + one line break is the content.

It can be broken into multiple chunks like so.
"""


class Prompt(Model):
    name: str
    content: str

    @classmethod
    def from_docstring(cls, docstring: str):
        lines = docstring.strip().split("\n")
        name = lines[0].strip()
        content_start = 3
        content = "\n".join(lines[content_start:]).strip()
        return cls(name=name, content=content)

    @property
    def model(self):
        return {
            "role": "system",
            "content": f"{self.name}\n{self.content}]",
        }


class Param(Model):
    type: str
    name: str
    description: str
    items: Optional[List[Any]] = None

    @property
    def model(self):
        prop = {"type": self.type, "description": self.description}
        if self.type == "enum":
            prop["enum"] = self.items
        elif self.type == "array":
            prop["array"] = self.items
        return prop


class Params(Model):
    parameters: List[Param]

    @property
    def model(self):

        return {
            "type": "object",
            "properties": {p.name: p.model for p in self.parameters},
            "additionalProperties": False,
            "required": [p.name for p in self.parameters],
        }


class CatalogType(Enum):
    FileSystem = "FileSystem"
    Database = "Database"
    Graph = "Graph"
    Collection = "Collection"


class Node(Model):
    name: str
    path: str
    content: Optional[Block] = None
    children: List[Node] = Field(default_factory=list)
    parent_id: Optional[str] = None
    relationships: Dict[str, List[str]] = Field(default_factory=dict)

    def add_child(self, node: Node):
        node.parent_id = self.id
        self.children.append(node)

    def find_by_path(self, path: str) -> Optional[Node]:
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
