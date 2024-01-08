import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


from scint.core.messages import Message, AssistantMessage, SystemMessage
from scint.core.tools import Tool
from scint.services.logger import log


class ClassifyMessage(Tool):
    description = (
        "Use this function to respond to the user and classify their messages."
    )
    props = {
        "keywords": {
            "type": "string",
            "description": "Generate up to three keyword, separated by commas, to categorize the message.",
        },
        "named_entities": {
            "type": "string",
            "description": "List any named entities, separated by commas, to categorize the message.",
        },
    }
    required = ["keywords", "named_entities"]

    async def execute_action(self, **kwargs):
        try:
            results = kwargs.get("results")
            yield AssistantMessage(results, self.name)

        except Exception as e:
            log.error(f" {e}")
            yield SystemMessage(e, self.name)


class ExtractContext(Tool):
    description = "This function extracts keywords, named entities, and summaries of messages and conversations."
    props = {
        "keywords": {
            "type": "string",
            "description": "Generate up to three keyword, separated by commas, to categorize the message.",
        },
        "named_entities": {
            "type": "string",
            "description": "List any named entities, separated by commas, to categorize the message.",
        },
        "summary": {
            "type": "string",
            "description": "Provide a concise but generic summary of the message which retains the author's perspective. Avoid using named entities and keywords to avoid data duplication.",
        },
    }
    required = ["keywords", "named_entities"]

    async def execute_action(self, **kwargs):
        try:
            results = kwargs.get("results")
            yield AssistantMessage(results, self.name)

        except Exception as e:
            log.error(f" {e}")
            yield SystemMessage(e, self.name)


class Classification(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created: datetime = Field(default_factory=datetime.now)
    content_summary: Optional[str]
    named_entities: Optional[List[str]]
    keywords: Optional[List[str]]


class Context:
    messages: List[Message] = []

    def add(self, message: Message):
        self.messages.append(message)


class ContextController:
    def __init__(self):
        pass

    def get_global_context(self):
        return self.global_context.messages

    def get_process_context(self, component):
        return self.component_context.get(component, Context())
