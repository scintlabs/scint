from typing import Any, Dict, List

from scint.framework.models import Model

from scint.framework.models.events import MethodCall


class Function(Model):
    name: str
    description: str
    parameters: Dict[str, Any]
    function_calls: List[MethodCall] = []

    @property
    def index(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
                "strict": True,
            },
        }

    async def append(self, call: MethodCall):
        self.function_calls.append(call)
        return await self.execute(**call.arguments)

    async def execute(self, *args, **kwargs):
        return await self.function(*args, **kwargs)
