import asyncio
from typing import Dict, List
from uuid import UUID

from core.util import generate_timestamp, generate_uuid4
from services.logger import log
from services.openai import generate_embedding, generate_summary


class Message:
    def __init__(self, role, content):
        self.id: UUID = generate_uuid4()
        self.created: str = generate_timestamp()
        self.role: str = role
        self.content: str = content
        self.content_summary: str = None
        self.content_embedding: List[float] = None

    def context_dump(self, summary=False):
        if summary:
            return {
                "role": self.role,
                "content": self.content_summary,
            }

        else:
            return {
                "role": self.role,
                "content": self.content,
            }

    def data_dump(self):
        message_data = {
            "id": str(self.id),
            "created": self.created,
            "role": self.role,
            "content": self.content,
            "content_summary": self.content_summary,
            "content_embedding": self.content_embedding,
        }

        return message_data


class Context:
    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, message):
        self.messages.append(message)


class ContextController:
    def __init__(self, max_full_messages: int, summarized_messages: int):
        self.context = Context()
        self.max_full_messages = max_full_messages
        self.summarized_messages = summarized_messages

    def add_message(self, message: Message):
        self.context.add_message(message)
        asyncio.create_task(self._process_message(message))

    def build_context(self):
        current_context = []
        max_full_messages = min(self.max_full_messages, len(self.context.messages))
        summarized_range = max(
            0,
            len(self.context.messages)
            - self.max_full_messages
            - self.summarized_messages,
        )
        summarized_messages = self.context.messages[summarized_range:-max_full_messages]

        for message in summarized_messages:
            summary_message = message.context_dump(summary=True)
            current_context.append(summary_message)

        for message in self.context.messages[-max_full_messages:]:
            full_message = message.context_dump()
            current_context.append(full_message)

        return current_context

    async def process_message(self, message, get_embedding=False) -> Message:
        log.info(f"Processing message.")

        message.content_summary = await self.summarize_content(message.content)

        if get_embedding:
            message.content_embedding = await generate_embedding(message.content)

        return message

    async def _process_message(self, message):
        processed_message = await self.process_message(message)

        if processed_message and isinstance(processed_message, Message):
            for i, msg in enumerate(self.context.messages):
                if msg.id == processed_message.id:
                    self.context.messages[i] = processed_message
                    break

            self.build_context()

    async def summarize_content(self, content):
        if len(content) > 150:
            summarized_content = await generate_summary(content)
            return summarized_content

        else:
            return content

    async def generate_embedding(self, content):
        message_embedding = await generate_embedding(content)
        return message_embedding

    def get_messages(self) -> List[Message]:
        return self.context.messages

    def get_context(self) -> List[Dict[str, str]]:
        return self.context.build_context()
