from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from core.config import DEFAULT_CONFIG
from core.memory import ContextController
from core.util import generate_uuid4
from services.logger import log


class AgentMatrix:
    def __init__(
        self,
        name: str,
        personality: str,
        guidelines: str = None,
        system_status: str = None,
    ) -> Dict[str, str]:
        self.name = name
        self.personality = personality
        self.guidelines = guidelines
        self.system_status = system_status

    def to_dict(self):
        return {
            "role": "system",
            "content": f"""{self.personality}\n\n{self.guidelines}\n\n{self.system_status}""",
        }


class AgentFunction:
    def __init__(self, name: str, desc: str, params: Dict[str, Any], req: List[str]):
        self.name = name
        self.description = desc
        self.params = params
        self.req = req

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.params,
            "required": self.req,
        }


class Agent(ABC):
    def __init__(self, config=DEFAULT_CONFIG):
        self.id: UUID = generate_uuid4()
        self.matrix = AgentMatrix(
            name="Assistant",
            personality="You are helpful assistant.",
            guidelines="Play nice.",
            system_status="Functioning normally.",
        )
        self.function = AgentFunction(
            name="function",
            desc="This is the default function.",
            params={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Describe the requested task in detail so the Coordinator can assign the appropriate worker.",
                    },
                },
            },
            req=["task"],
        )
        self.context = ContextController(4, 10)
        self.config = config

    async def get_state(self) -> Dict[str, Any]:
        matrix = self.matrix.to_dict()
        function = [self.function.to_dict()]
        context = self.context.build_context()
        messages = [matrix]

        for message in context:
            messages.append(message)

        self.state = {
            "model": self.config.get("model"),
            "temperature": self.config.get("temperature"),
            "top_p": self.config.get("top_p"),
            "max_tokens": self.config.get("max_tokens"),
            "presence_penalty": self.config.get("presence_penalty"),
            "frequency_penalty": self.config.get("frequency_penalty"),
            "messages": messages,
            "functions": function,
        }

        return self.state

    @abstractmethod
    async def process_request(self):
        pass

    @abstractmethod
    async def eval_function(self):
        pass
