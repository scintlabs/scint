from __future__ import annotations

import json

from typing import Any, Dict, TypeVar

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI, OpenAI

from scint.lib.schema.signals import Response
from scint.lib.types import Struct, Trait
from scint.lib.schema.signals import Message, FunctionCall


_T = TypeVar("_T")


class Configuration(Struct): ...


class Providers(Struct):
    openai: AsyncOpenAI = AsyncOpenAI()
    openai_sync: OpenAI = OpenAI()
    anthropic: AsyncAnthropic = AsyncAnthropic()


class Intelligent(Trait):
    async def process(self):
        req: Dict[str, Any] = {
            "model": "gpt-4o",
            "temperature": 1.4,
            "top_p": 0.6,
            "response_format": Response,
            **self.model,
        }

        print(self.context.messages[-1].content)

        res = await Providers.openai.beta.chat.completions.parse(**req)
        messages = self.context.messages

        if res.choices[0].message.parsed:
            data = res.choices[0].message.parsed
            messages.append(data)

        if res.choices[0].message.tool_calls:
            for call in res.choices[0].message.tool_calls:
                messages.append(
                    FunctionCall(
                        call_id=call.id,
                        name=call.function.name,
                        arguments=json.loads(call.function.arguments),
                    )
                )
        return True

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
                # c = FunctionCall(
                #     call_id=call.id,
                #     name=call.function.name,
                #     arguments=json.loads(call.function.arguments),
                # )
                func_name = call.function.name
                args = json.loads(call.function.arguments)
                func = getattr(self, func_name)
                print(func_name, args)
                return await func(args)

        return True

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
