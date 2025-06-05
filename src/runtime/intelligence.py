from __future__ import annotations

import json
import random
from typing import Any, TypeAlias, TypeVar, Union, Dict, List

from attrs import asdict, define, field

from src.base.records import Message
from src.resources.outlines import Result
from src.services.models import completion, response

T = TypeVar("T")
Content: TypeAlias = Union[str, List[str], Dict[str, Any]]


@define
class ModelConfig:
    model: str = field(default="gpt-4.1")
    top_p: float = field(default=round(random.uniform(0.5, 1), 2))
    temperature: float = field(default=round(random.uniform(0.9, 1.7), 2))


def load_instructions(name: str):
    with open("config/instructions.json", "r") as f:
        content = f.read()
        for i in json.loads(content):
            if i.get("name") == name.lower():
                return i.get("content")


async def generate(self, context):
    async def build_request(context):
        instructions = load_instructions(type(self).__name__)
        print(instructions)
        context = await context.build()

        return {
            "input": context,
            "instructions": instructions,
            "text": {"format": self.serialize(self.format)},
            **asdict(self.config),
        }

    async def handle_request(req):
        res = await response(req)
        print(res)
        for obj in res.output:
            match obj.type:
                case "message":
                    async for msg in handle_message(obj):
                        yield msg
                case "function_call":
                    async for call_res in handle_execution(obj):
                        yield call_res

    async def handle_message(message):
        for obj in message.content:
            yield Message(**json.loads(obj.text))

    async def handle_execution(execution):
        for func in self.tools:
            if execution.name == func.__name__:
                args = json.loads(execution.arguments)
                res = await func(**args)
                yield Result(execution.call_id, execution.name, str(res))

    req = await build_request(context)
    async for res in handle_request(req):
        await context.update(res)
        if isinstance(res, Result):
            async for out in generate(context):
                yield out
        yield res


async def execution():
    req = {
        "model": "gpt-4.1",
        "top_p": round(random.uniform(0.5, 1), 2),
        "temperature": round(random.uniform(0.9, 1.7), 2),
        "tool_choice": "required",
    }
    res = await completion(**req)
    return res.choices[0].message.parsed


async def description(obj: Any, kind: str, /, val: str = None):
    req = {
        "model": "gpt-4.1",
        "top_p": round(random.uniform(0.5, 1), 2),
        "temperature": round(random.uniform(0.9, 1.7), 2),
    }

    if kind == "function":
        msg = "Generate a description for this function, which is used in the `description` field when serializing it. Avoid describing implementation details and simply provide a general description of the object and what it's used for in one or two sentences:"
        req["input"] = f"{msg}\n\n{obj}"

    elif kind == "session":
        msg = "Generate a name and description for this conversation, which is used to populate the class object's `name` and `description` fields. Simple provide a concise name in the form of a title and a one-sentence description. Return the name on the first line and the description on the second line."
        req["input"] = f"{msg}\n\n{obj}"

    elif kind == "parameter":
        msg = f"{val} is a parameter for the following function:\n\n{obj}\n\nPlease generate a single sentence describing the parameter."
        req["input"] = msg

    res = await response(**req)
    if res.output_text is not None:
        return res.output_text
