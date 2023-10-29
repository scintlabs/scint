from abc import ABC, abstractmethod
from typing import Dict, List, Any

from services.logger import log
from core.config import GPT4


class Agent(ABC):
    def __init__(self, name, system_init, function, config):
        self.name: str = name
        self.system_init: Dict[str, str] = system_init
        self.context: List[Dict[str, str]] = [self.system_init]
        self.function: Dict[str, Any] = function
        self.config: Dict[str, Any] = config

    async def state(self) -> Dict[str, Any]:
        log.info(f"Getting {self.name} state.")

        config = await self.get_config()
        context = []
        for item in self.context:
            context.append(item)

        state = {
            "messages": context,
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

    async def format_message(self, role, content, name) -> Dict[str, str]:
        log.info("Formatting message.")

        reply = {
            "role": role,
            "content": content,
            "name": name,
        }

        return reply

    @abstractmethod
    async def process_request(self, request):
        pass

    @abstractmethod
    async def eval_function_call(self, res_message):
        pass
