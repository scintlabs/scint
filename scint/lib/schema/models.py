from __future__ import annotations


from typing import List, Optional, Any

from pydantic import BaseModel, ConfigDict

from scint.lib.schema.signals import Content


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Prompt(Model):
    name: str
    description: str
    keywords: List[str]
    content: Content

    @property
    def model(self):
        return {"role": "system", "content": self.content.content}


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
            "required": [p.name for p in self.parameters],
            "additionalProperties": False,
        }
