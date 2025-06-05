from __future__ import annotations

import json
from typing import List, Dict, Any

from attrs import define, field

from src.services.models import response


@define
class Metadata:
    name: str = field(default=None)
    description: str = field(default=None)
    embedding: List[float] = field(factory=list, repr=False)
    annotations: List[str] = field(factory=list)
    keywords: List[str] = field(factory=list)
    events: List[Dict[str, Any]] = field(factory=list)

    async def build(cls):
        res = await response(
            input=f"Generate concise, intelligent, semantically-rich metadata for the following thread:\n\n{await cls.render()}",
            text={"format": cls.serialize(Metadata)},
            model="gpt-4.1",
        )
        for obj in res.output:
            if obj.type == "message":
                for content in obj.content:
                    text = json.loads(content.text)
                    return cls(**text)
