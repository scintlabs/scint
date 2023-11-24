import asyncio
from uuid import UUID
from typing import Dict, List, Any

from services.logger import log
from services.openai import embedding, summary
from core.artifacts import File
from core.util import generate_timestamp, generate_uuid4


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
        log.info(summarized_content)

        return summarized_content

    else:
        return content


async def process_message(message, get_embedding=False):
    log.info(f"Processing message.")

    message.content_summary = await summarize_content(message.content)

    if get_embedding:
        message.content_embedding = await generate_embedding(message.content)


async def generate_embedding(content):
    message_embedding = await embedding(content)
    return message_embedding


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

    def dump(self, summary=False):
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


class Context:
    def __init__(self):
        self.messages: List[Message] = []
        self.current_context: List[Dict[str, str]] = []

    def add_message(self, message):
        self.messages.append(message)
        self.current_context.append(message.dump())


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
            self.context.add_message(processed_message)
            self.build_context()

    def build_context(self):
        new_context: List[Dict[str, str]] = []
        summary_start_index = max(len(self.context.messages) - self.max_summary, 0)
        full_start_index = max(
            len(self.context.messages) - self.max_full, summary_start_index
        )

        for message in reversed(self.context.messages[full_start_index:]):
            if message:
                full_message = message.dump()
                new_context.append(full_message)

        for message in reversed(
            self.context.messages[summary_start_index:full_start_index]
        ):
            if message:
                summary_message = message.dump(summary=True)
                new_context.append(summary_message)

        self.context.current_context = new_context

    def get_messages(self) -> List[Message]:
        messages = []

        for message in self.context.messages:
            message_dict = message.dump()
            messages.append(message_dict)

        return messages

    def get_context(self) -> List[Dict[str, str]]:
        return self.context.current_context
