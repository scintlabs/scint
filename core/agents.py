from abc import ABC, abstractmethod
from typing import Dict, Any

from services.logger import log
from core.config import DEFAULT_INIT, DEFAULT_CONFIG
from core.memory import ContextController


class StateMachine(ABC):
    def __init__(self, name):
        self.name: str = name


class Actor(ABC):
    def __init__(self, name, config=DEFAULT_CONFIG, system_init=DEFAULT_INIT):
        self.name: str = name
        self.config: Dict[str, Any] = config
        self.system_init: Dict[str, str] = system_init
        self.function: Dict[str, Any] | None
        self.context_controller = ContextController(4)

    async def get_state(self) -> Dict[str, Any]:
        log.info(f"Getting {self.name}'s state.")

        self.messages = [self.system_init]
        self.context = self.context_controller.get_context()

        for message in self.context:
            self.messages.append(message)

        self.state = {
            "messages": self.messages,
            "model": self.config.get("model"),
            "max_tokens": self.config.get("max_tokens"),
            "presence_penalty": self.config.get("presence_penalty"),
            "frequency_penalty": self.config.get("frequency_penalty"),
            "top_p": self.config.get("top_p"),
            "temperature": self.config.get("temperature"),
        }

        if self.function is not None:
            self.state["functions"] = [self.function]
            self.state["function_call"] = {"name": self.name}

        return self.state
