import os
import asyncio
import threading
from collections import deque
from typing import Dict, List, Any

from services.logger import log
from services.openai import embedding, summary
from core.util import generate_timestamp, generate_uuid4


class MemoryManager:
    def __init__(self):
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
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(ContextController, cls).__new__(cls)
                log.info(f"ContextController: initializing self.")

        return cls._instance

    def __init__(self, max_messages: int) -> None:
        self.max_messages = max_messages
        self.context = deque(maxlen=max_messages)
        self.memory_manager = MemoryManager()

    def add_message_sync(self, message):
        log.info(f"ContextController: adding message to context synchronously.")
        self.context.append(message)

        if len(self.context) == self.max_messages:
            self.summarize_oldest_message()

    async def add_message(self, message):
        log.info(f"ContextController: adding message to context asynchronously.")
        await asyncio.to_thread(self.add_message_sync, message)

    def summarize_oldest_message(self):
        log.info(f"ContextController: starting message summarization in background.")

        oldest_message = self.context[-1]

        def summarize_and_update():
            summary = asyncio.run(self.memory_manager.generate_summary(oldest_message))
            self.context[-1] = summary

        threading.Thread(target=summarize_and_update).start()

    def get_context(self) -> List[Dict[str, Any]]:
        return list(self.context)
