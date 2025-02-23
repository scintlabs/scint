from __future__ import annotations

import json

from typing import Any, Dict, TypeVar

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI, OpenAI

from scint.lib.schemas.signals import Response, Result
from scint.lib.types import Struct, Trait
from scint.lib.schemas.signals import Message, ToolCall


_T = TypeVar("_T")


class Configuration(Struct): ...


class Providers(Struct):
    openai: AsyncOpenAI = AsyncOpenAI()
    openai_sync: OpenAI = OpenAI()
    anthropic: AsyncAnthropic = AsyncAnthropic()


class Intelligent(Trait):
    async def think(self):
        req = {
            "model": "gpt-4o",
            "temperature": 1.4,
            "top_p": 0.6,
            "response_format": Response,
            **self.model,
        }

        res = await Providers.openai.beta.chat.completions.parse(**req)

        if res.choices[0].message.parsed:
            data = res.choices[0].message.parsed
            self.context.update(self, data)

        if res.choices[0].message.tool_calls:
            for call in res.choices[0].message.tool_calls:
                call = ToolCall(
                    tool_call_id=call.id,
                    name=call.function.name,
                    arguments=json.loads(call.function.arguments),
                )
                self.update(call)
                func = getattr(self, call.name)
                res: Result = await func(**call.arguments)
                res.tool_call_id = call.tool_call_id
                self.update(res)
                self.context.update(self, data)
                return await self.think()


class Functional(Trait):
    async def process(self):
        req: Dict[str, Any] = {
            "model": "gpt-4o",
            "temperature": 1.1,
            "top_p": 0.8,
            **self.model,
        }

        res = await Providers.openai.chat.completions.create(**req)

        if res.choices[0].message.tool_calls:
            for call in res.choices[0].message.tool_calls:
                call = ToolCall(
                    tool_call_id=call.id,
                    name=call.function.name,
                    arguments=json.loads(call.function.arguments),
                )
                self.context.update(self, call)
                func = getattr(self, call.name)
                res: Result = await func(**call.arguments)
                res.tool_call_id = call.tool_call_id
                self.context.update(self, res)
                return await self.think()

    async def handle(self, obj: Any):
        self.context.messages.append(obj)
        if isinstance(obj, Message) and obj.role == "assistant":
            return self.callback(obj) if self.callback else self.output(obj)

        elif isinstance(obj, Message):
            res = await self.process(self.context)
            self.context.messages.append(obj)
            return await self.handle(res)

        elif isinstance(obj, ToolCall):
            func = getattr(self.impl, obj.name.context)
            res = await func(**obj.args)
            self.context.messages.append(obj)
            final_res = await self.process(self.context)
            self.update(final_res)
            return await self.handle(final_res)


def generate_embedding(input: str):
    req = {
        "model": "text-embedding-3-small",
        "input": str(input),
    }
    res = Providers.openai_sync.embeddings.create(**req)
    return res.data[0].embedding
