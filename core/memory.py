import asyncio
from typing import Dict, List, Any

from services.logger import log
from services.openai import embedding, summary
from core.util import generate_timestamp, generate_uuid4


async def generate_summary(message) -> Dict[str, str]:
    # log.info(f"ContextController: generating message summary.")

    if len(message) > 100:
        system_init: Dict[str, str] = {
            "role": "system",
            "content": "You are a compression algorithm for Scint, a state-of-the-art intelligent assistant. For every message, remove unnecessary content and compress the message for minimal contextual understanding using shorthand language. Use first person for assistant assistant messages and third person for user messages.",
            "name": "compression",
        }
        messages: List[Dict[str, str]] = [system_init, message]
        request: Dict[str, Any] = {"messages": messages}
        summarized_message = await summary(**request)

        return summarized_message

    else:
        return message


async def generate_embedding(content) -> List[float]:
    message_embedding = await embedding(content)

    return message_embedding


async def process_message(message, get_embedding=False) -> Dict[str, Any]:
    try:
        processed_message = {
            "id": generate_uuid4(),
            "timestamp": generate_timestamp(),
            "role": message.get("role"),
            "content": message.get("content"),
            "name": message.get("name"),
            "summary": await generate_summary(message),
        }

        if get_embedding == True:
            processed_message["embedding"] = await generate_embedding(
                message.get("content")
            )

        else:
            processed_message["embedding"] = None

        return processed_message

    except KeyError as e:
        log.error(f"KeyError encountered in process_message: {e}")
        raise


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ContextController(metaclass=SingletonMeta):
    def __init__(self, max_full, max_summary):
        if not hasattr(self, "initialized"):
            self.messages: List[Dict[str, Any]] = []
            self.context: List[Dict[str, Any]] = []
            self.max_full: int = max_full
            self.max_summary: int = max_summary
            self.initialized = True

    async def process_message(self, message):
        # log.info("ContextController: processing and updating message.")

        processed_message = await process_message(message)
        self.messages.append(processed_message)
        self.build_context()

    def build_context(self):
        # log.info(f"ContextController: building context from messages.")

        new_context = []
        summary_start_index = max(len(self.messages) - self.max_summary, 0)
        full_start_index = max(len(self.messages) - self.max_full, summary_start_index)

        for message in reversed(self.messages[full_start_index:]):
            new_context.append(
                {
                    "role": message["role"],
                    "content": message["content"],
                    "name": message["name"],
                }
            )

        for message in reversed(self.messages[summary_start_index:full_start_index]):
            new_context.append(
                {
                    "role": message["role"],
                    "content": message["summary"]["content"]
                    if "summary" in message
                    else message["content"],
                    "name": message["name"],
                }
            )

        self.context = new_context
        # log.info("ContextController: built new context.")

        return self.context

    def get_context(self) -> List[Dict[str, Any]]:
        # log.info(f"ContextController: getting context.")

        return list(self.context)

    def get_messages(self) -> List[Dict[str, Any]]:
        # log.info(f"ContextController: getting messages.")

        return list(self.messages)

    def add_message(self, message):
        # log.info("ContextController: adding message to context.")

        self.context.append(message)
        asyncio.create_task(self.process_message(message))
