from typing import Any, Dict, List, Union

from scint.providers import build_request, unpack_response

from scint.base.models import get_provider
from scint.base.models import Model
from scint.base.models.functions import Function
from scint.base.models.messages import Message, Prompt
from scint.base.types.containers import Parcel
from scint.base.utils.attrs import dictorial, keyfob


class FuncComponent(Parcel):
    name: str
    description: str
    parameters: Dict[str, Any]

    async def invoke(self, command):
        async def _call(request):
            paths = dictorial(get_provider("openai"), "response_paths")
            response = await unpack_response(request, paths)
            return response

        callable = dictorial(get_provider("openai"), f"format.completion.method")
        params = build_request(command)
        invocation = await callable(**params)
        arguments = await _call(invocation)
        return arguments

    def build(function):
        return {
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": keyfob(function, "name"),
                        "description": keyfob(function, "description"),
                        "parameters": keyfob(function, "parameters"),
                    },
                }
            ],
            "tool_choice": {
                "type": "function",
                "function": {"name": keyfob(function, "name")},
            },
        }

    async def function(self, *args, **kwargs):
        pass


class Chain(Model):
    instructions: List[Union[Prompt, Message]]
    functions: List[Function]


class Generator(Model):
    prompts: List[Prompt]
    functions: List[Function]
