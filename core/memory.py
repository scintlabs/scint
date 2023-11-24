import asyncio
from uuid import UUID
from typing import Dict, List

from services.logger import log
from services.openai import embedding, summary
from core.artifacts import File
from core.util import generate_timestamp, generate_uuid4


class Message:
    def __init__(self, role, content, name=None):
        self.id: UUID = generate_uuid4()
        self.created: str = generate_timestamp()
        self.role: str = role
        self.name: str = name
        self.content: str = content
        self.content_summary: str = None
        self.content_embedding: List[float] = None
        self.files: List[File] = []

    def context_dump(self, summary=False):
        if summary:
            return {
                "role": self.role,
                "content": self.content_summary,
                "name": self.name,
            }

        else:
            return {
                "role": self.role,
                "content": self.content,
                "name": self.name,
            }

    def data_dump(self, summary=False):
        message_data = {
            "id": str(self.id),
            "created": self.created,
            "role": self.role,
            "name": self.name,
            "content": self.content,
            "content_summary": self.content_summary,
        }

        return message_data


async def summarize_content(content):
    if len(content) > 150:
        system_init = {
            "role": "system",
            "content": "You are a compression algorithm for Scint, a state-of-the-art intelligent assistant. For every message, remove unnecessary content and compress the message for minimal contextual understanding using shorthand language. Don't change message perspective—just compress the content.",
            "name": "summarize",
        }
        message = {"role": "system", "content": content, "name": "message_to_summarize"}
        messages = [system_init, message]
        request = {"messages": messages}
        summarized_message = await summary(**request)
        summarized_content = summarized_message.get("content")

        return summarized_content

    else:
        return content


async def process_message(message, get_embedding=False) -> Message:
    log.info(f"Processing message.")

    message.content_summary = await summarize_content(message.content)

    if get_embedding:
        message.content_embedding = await generate_embedding(message.content)

    return message


async def generate_embedding(content):
    message_embedding = await embedding(content)
    return message_embedding


class Context:
    def __init__(self):
        self.current_context: List[Dict[str, str]] = []
        self.messages: List[Message] = []

    def add_message(self, message):
        self.current_context.append(message.context_dump())
        self.messages.append(message)


class ContextController:
    def __init__(self, max_full, max_summary):
        self.context = Context()
        self.max_full: int = max_full
        self.max_summary: int = max_summary

    def add_message(self, message):
        if isinstance(message, dict):
            message = Message(**message)

        self.context.add_message(message)
        asyncio.create_task(self._process_message(message))

    async def _process_message(self, message):
        processed_message = await process_message(message)

        if processed_message and isinstance(processed_message, Message):
            for i, msg in enumerate(self.context.messages):
                if msg.id == processed_message.id:
                    self.context.messages[i] = processed_message
                    break

            self.build_context()

    def build_context(self):
        new_context = []
        full_messages = self.context.messages[-self.max_full :]
        summary_messages = self.context.messages[-self.max_summary : -self.max_full]

        for message in full_messages:
            full_message = message.context_dump()
            new_context.append(full_message)

        for message in summary_messages:
            summary_message = message.context_dump(summary=True)
            new_context.append(summary_message)

        self.context.current_context = new_context

        if len(self.context.messages) > self.max_summary:
            self.context.messages = self.context.messages[-self.max_summary :]

    def get_messages(self) -> List[Message]:
        return self.context.messages

    def get_context(self) -> List[Dict[str, str]]:
        return self.context.current_context
