from typing import Dict, List, Any

import asyncio

from services.logger import log
from services.openai import embedding, summary
from core.util import generate_timestamp, generate_uuid4


class MemoryManager:
    def __init__(self):
        log.info(f"MemoryManager: initializing self.")

        self.full_messages: List[Dict[str, str]] = []
        self.summarized_messages: List[Dict[str, str]] = []

    async def generate_summary(self, message) -> Dict[str, str]:
        log.info(f"MemoryManager: generating message summary.")

        self.system_init: Dict[str, str] = {
            "role": "system",
            "content": "Conversation summarizer, Hemingway's brevity. Condense discussions, minimum context, third person.",
            "name": "summarizer",
        }
        self.messages: List[Dict[str, str]] = [self.system_init, message]
        self.request: Dict[str, Any] = {"messages": self.messages}
        summarized_message = await summary(**self.request)

        return summarized_message

    async def generate_embedding(self, content) -> List[float]:
        message_embedding = await embedding(content)
        return message_embedding

    async def process_message(self, message, get_embedding=False) -> Dict[str, Any]:
        log.info(f"MemoryManager: processing message: {message}.")

        role = message.get("role")
        content = message.get("content")
        name = message.get("name")
        summary = await self.generate_summary(message)

        if get_embedding == True:
            embedding = await self.generate_embedding(content)

        else:
            embedding = None

        processed_message = {
            "id": generate_uuid4(),
            "timestamp": generate_timestamp(),
            "role": role,
            "content": content,
            "name": name,
            "summary": summary,
            "embedding": embedding,
        }

        log.info(f"MemoryManager: processed message: {processed_message}.")

        return processed_message


class ContextController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ContextController, cls).__new__(cls)  # Only pass cls
        return cls._instance

    def __init__(self, max_messages: int) -> None:
        log.info(f"ContextController: initializing self.")

        self.max_messages = max_messages
        self.context: List[Dict[str, Any]] = []
        self.memory_manager = MemoryManager()

    async def add_message(self, message):
        log.info(f"ContextController: adding message to context.")

        processed_message = await self.memory_manager.process_message(message)
        self.context.append(processed_message)

        while len(self.context) > 2 * self.max_messages:
            for i, msg in enumerate(self.context):
                if "summary" in msg and msg["content"] == msg["summary"]["content"]:
                    self.context.pop(i)
                    break

        non_summarized_msgs = [
            msg for msg in self.context if msg["content"] != msg["summary"]["content"]
        ]

        if len(non_summarized_msgs) > self.max_messages:
            oldest_non_summarized = non_summarized_msgs[0]
            oldest_non_summarized["content"] = oldest_non_summarized["summary"][
                "content"
            ]

    def get_context(self) -> List[Dict[str, Any]]:
        stripped_context = []

        for message in self.context:
            stripped_message = {
                "role": message["role"],
                "content": message["content"],
                "name": message["name"],
            }
            stripped_context.append(stripped_message)

        return stripped_context
