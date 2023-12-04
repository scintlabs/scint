from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from scint.core.memory import ContextController, Message
from scint.core.util import generate_uuid4
from scint.services.logger import log


class AgentMatrix(ABC):
    def __init__(
        self,
        name: str,
        personality: str,
        guidelines: str = None,
        system_status: str = None,
    ):
        self.name = name
        self.personality = personality
        self.guidelines = guidelines
        self.system_status = system_status

    def to_dict(self) -> Dict[str, str]:
        return {
            "role": "system",
            "content": f"""{self.personality}\n\n{self.guidelines}\n\n{self.system_status}""",
        }


class AgentTool(ABC):
    def __init__(self, name: str, desc: str, params: Dict[str, Any], req: List[str]):
        self.name = name
        self.description = desc
        self.params = params
        self.req = req

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.params,
                "required": self.req,
            },
        }

    async def evaluate(self, name, **kwargs):
        log.info(f"Tool: evaluating {name} call.")

        if name != self.name:
            raise ValueError(
                f"Incorrect tool name. Expected '{self.name}', got '{name}'."
            )

        param_keys = self.params.get("properties", {}).keys()
        for key in kwargs.keys():
            if key not in param_keys:
                raise ValueError(
                    f"Invalid parameter '{key}'. Expected parameters: {list(param_keys)}."
                )

        for req_param in self.req:
            if req_param not in kwargs:
                raise ValueError(f"Missing required parameter '{req_param}'.")

        async for result in self.function(**kwargs):
            yield result

    @abstractmethod
    async def function(self, **kwargs) -> Message:
        pass


class Agent(ABC):
    def __init__(self, config):
        self.id: UUID = generate_uuid4()
        self.matrix: AgentMatrix = None
        self.tools: AgentTool = None
        self.context = ContextController(4, 10)
        self.config = config

    async def get_state(self) -> Dict[str, Any]:
        matrix = self.matrix.to_dict()
        messages = [matrix]
        tools = [self.tools.to_dict()]
        context = self.context.build_context()

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
            "tools": tools,
        }

        return self.state

    @abstractmethod
    async def process_request(self, request: Message) -> Message:
        pass
