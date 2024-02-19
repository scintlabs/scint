from typing import Optional

from scint.components.models import AssistantMessage, SystemMessage
from scint.components.process import Preset, Process
from scint.components.tool import Tool


class Expand(Tool):
    description = "Transform topics through breadth and depth transformations."
    props = {
        "depth": {
            "type": "string",
            "description": "Add a deeper, more detailed statement or question within the same topic.",
        },
        "breadth": {
            "type": "string",
            "description": "Add statements or questions within an orthogonally related topic.",
        },
    }

    async def function(self, depth: str, breadth: str):
        content = f"{depth} {breadth}"
        yield AssistantMessage(content=content, sender="Expand", receiver="User")


class Transform(Process):
    Preset = Preset.assistant
    description = "You are a recursive transforming function. For every message, recursively transform the content."
    tooling = [Expand()]


organize = {
    "system_init": "You are a refactoring function for an artificial intelligence system. For every message, group sentences into subtopics and label them.",
    "config": {},
    "functions": [],
}

clarify = {
    "system_init": "You are a refactoring function for an artificial intelligence system. For every statement or question, remove redundancy and improve clarity.",
    "config": {},
    "functions": [],
}
