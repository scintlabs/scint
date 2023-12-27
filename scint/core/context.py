from datetime import datetime
from typing import Dict, List
from uuid import UUID

from scint.core.messages import Message
from scint.services import openai
from scint.services.logger import log
from scint.util import generate_timestamp, generate_uuid4


class Memory:
    def __init__(self):
        self.id: UUID = generate_uuid4()
        self.created: datetime.datetime = generate_timestamp()
        self.modified: datetime.datetime = generate_timestamp()
        self.messages: List[Message] = []
        self.keywords: List[str] = []
        self.embedding: List[int] = []
        self.summary: str = None


class Heuristic:
    def __init__(self):
        self.memory: Memory
        self.keywords: List[str] = []
        self.named_entities: List[str] = []
        self.embedding: List[int] = []
        self.summary: str = None


class Context:
    def __init__(self):
        self.id: UUID = generate_uuid4()
        self.created: datetime.datetime = generate_timestamp()
        self.modified: datetime.datetime = generate_timestamp()
        self.messages: List[Message] = []
        self.keywords: List[str] = []
        self.embeddings: List[int] = []
        self.summary: str = None


class ContextController:
    def __init__(self):
        self.name = "ContextController"
        self.global_context = Context()
        self.component_context = {
            "Persona": Context(),
            "Coordinator": Context(),
        }

        log.info(f"{self.name} loaded.")

    def add_message(self, message: Message, component=None):
        if component is not None:
            self.component_context[component].messages.append(message)
            log.info(f"ContextController: message added to {component} context.")

        else:
            self.global_context.messages.append(message)
            log.info(f"ContextController: message added to global context.")

    def get_global_context(self):
        return self.global_context.messages

    def get_component_context(self, component):
        return self.component_context.get(component, Context())

    async def _summarize(self, data):
        if isinstance(data, str):
            summarized_string = await openai.summary(data)
            return summarized_string

        elif isinstance(data, Message):
            for i, msg in enumerate(self.memory.messages):
                if msg.id == data.id:
                    if data.content_summary is not None:
                        summarized_content = await summary(data.content)
                        self.memory.messages[i].content_summary = summarized_content

        elif isinstance(data, Memory):
            summary = " ".join([msg.content + "\n\n" for msg in data.messages])
            if summary:
                data.summary = await summary(summary)

    async def _build_episodic_memory(self, messages: List[Message]):
        try:
            conversation = ""
            message_ids = []
            self.embedding = await openai.embedding(conversation)

            for message in messages:
                message_ids.append(message.id)
                conversation += f"{message.data_dump()}"

            return {
                "id": generate_uuid4(),
                "messages": self.message_ids,
                "embedding": self.embedding,
            }

        except Exception as e:
            log.info(f"MemoryController: {e} exception during build process.")
