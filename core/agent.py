import json
import importlib
from abc import ABC, abstractmethod
from typing import Dict, List, Any

from services.logger import log
from core.message import Message
from core.config import GPT4


class Agent(ABC):
    def __init__(self, name, system_init, function, config):
        log.info(f"Initializing Scint interface.")

        self.name = name
        self.system_init: Dict[str, str] = system_init
        self.messages: List[Dict[str, str]] = [self.system_init]
        self.function: Dict[str, Any] = function
        self.config: Dict[str, Any] = config

    async def state(self) -> Dict[str, Any]:
        log.info(f"Getting interface state.")

        config = await self.get_config()
        messages = []
        for m in self.messages:
            messages.append(m)

        state = {
            "messages": messages,
            "functions": [self.function],
            "model": config.get("model"),
            "max_tokens": config.get("max_tokens"),
            "presence_penalty": config.get("presence_penalty"),
            "frequency_penalty": config.get("frequency_penalty"),
            "top_p": config.get("top_p"),
            "temperature": config.get("temperature"),
        }

        return state

    async def get_config(self, config_dict=None) -> Dict[str, Any]:
        if config_dict is None:
            config_dict = {}

        config = {
            "model": config_dict.get("model", GPT4),
            "temperature": config_dict.get("temperature", 1),
            "top_p": config_dict.get("top_p", 1),
            "presence_penalty": config_dict.get("presence_penalty", 0.3),
            "frequency_penalty": config_dict.get("frequency_penalty", 0.3),
            "max_tokens": config_dict.get("max_tokens", 4096),
        }

        return config

    @abstractmethod
    async def eval_function_call(self, res_message):
        pass

    @abstractmethod
    async def process_request(self, payload):
        pass

    async def generate_reply(self, res_message):
        log.info("Generating reply.")

        role = res_message.get("role")
        content = res_message.get("content")

        if not role or not content:
            log.error("Role or content missing in res_message.")
            return

        reply_message: dict[str, str] = {
            "role": role,
            "content": content,
            "name": self.name,
        }

        reply = Message(
            sender=self.name,
            recipient="user",
            message_data=reply_message,
        )

        return reply
