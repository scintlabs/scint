from __future__ import annotations

import json

from typing import Any, Dict, TypeVar

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI, OpenAI

from scint.lib.schema.signals import Response
from scint.lib.struct import Struct
from scint.lib.traits import Trait
from scint.lib.schema.signals import Message, FunctionCall


_T = TypeVar("_T")


class Configuration(Struct): ...


class Providers(Struct):
    openai: AsyncOpenAI = AsyncOpenAI()
    openai_sync: OpenAI = OpenAI()
    anthropic: AsyncAnthropic = AsyncAnthropic()


class Intelligent(Trait):
    async def process(self, context):
        req: Dict[str, Any] = {
            "model": "gpt-4o",
            "temperature": 1.4,
            "top_p": 0.6,
            "response_format": Response,
            **context.model,
        }

        res = await Providers.openai.beta.chat.completions.parse(**req)

        if res.choices[0].message.parsed:
            context.messages.append(res.choices[0].message.parsed)

        if res.choices[0].message.tool_calls:
            context.messages.append(res.choices[0].message)
            for call in res.choices[0].message.tool_calls:
                context.messages.append(
                    FunctionCall(
                        id=call.id,
                        name=call.function.name,
                        arguments=json.loads(call.function.arguments),
                    )
                )
        return context.messages[-1]

    async def handle(self, obj: Any):
        self.context.messages.append(obj)
        if isinstance(obj, Message) and obj.role == "assistant":
            return self.callback(obj) if self.callback else self.output(obj)

        elif isinstance(obj, Message):
            res = await self.process(self.context)
            self.context.messages.append(obj)
            return await self.handle(res)

        elif isinstance(obj, FunctionCall):
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
