from __future__ import annotations

import json
from typing import Any, List, Type

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI, OpenAI

from src.types.models import FunctionCall
from src.types.structure import Struct


class ModelProviders(Struct):
    openai_sync: OpenAI = OpenAI()
    openai: AsyncOpenAI = AsyncOpenAI()
    anthropic: AsyncAnthropic = AsyncAnthropic()


async def parse(self, agent: Type, **req):
    res = await ModelProviders.openai.beta.chat.completions.parse(**req)
    msg = res.choices[0].message
    agent.context.update(msg.parsed)
    if msg.tool_calls and msg.tool_calls[0] is not None:
        await self.execute(agent, msg.tool_calls)
    return msg.parsed


async def execute(self, agent: Type, tool_calls: List[FunctionCall]):
    while tool_calls:
        for tool_call in tool_calls:
            call = FunctionCall(
                call_id=tool_call.id,
                name=tool_call.function.name,
                arguments=json.loads(tool_call.function.arguments),
            )
            agent.context.update(call)

            if hasattr(self, call.name):
                res = await getattr(self, call.name)(**call.arguments)
                res.tool_call_id = call.call_id
                agent.context.update(res)
                message = await self.parse()
            else:
                print(f"Tool {call.name} unavailable.")
    return message


async def process(self, agent: Type):
    pass


async def compose(self, context: Any = None, schema: Any = None):
    cfg = self.configure().context(context).request()
    res = await ModelProviders.openai.beta.chat.completions.parse(**cfg)
    return json.loads(res.choices[0].message.content)


async def classify(input: str):
    req = {"model": "text-embedding-3-small", "input": str(input)}
    return await ModelProviders.openai.embeddings.create(**req).data[0].embedding


class entrypoint:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __set_name__(self, owner, name):
        self.name = name

        def __call__(self_instance, *args, **kwargs):
            method = getattr(self_instance, name)
            return method(*args, **kwargs)

        owner.__call__ = __call__
        setattr(owner, name, self.func)


class caller:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __set_name__(self, owner, name):
        self.name = name

        def __call__(self_instance, *args, **kwargs):
            method = getattr(self_instance, name)
            return method(*args, **kwargs)

        owner.__call__ = __call__
        setattr(owner, name, self.func)
