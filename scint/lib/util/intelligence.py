from __future__ import annotations

import json

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI, OpenAI

from scint.lib.schemas.signals import Response
from scint.lib.types import Struct, Trait
from scint.lib.schemas.signals import ToolCall


class Configuration(Struct): ...


class Providers(Struct):
    openai_sync: OpenAI = OpenAI()
    openai: AsyncOpenAI = AsyncOpenAI()
    anthropic: AsyncAnthropic = AsyncAnthropic()


def config(model):
    return {
        "model": "gpt-4o",
        "temperature": 1.4,
        "top_p": 0.6,
        "response_format": Response,
        **model,
    }


class Intelligent(Trait):
    async def think(self):
        if r := await Providers.openai.beta.chat.completions.parse(
            **config(self.model)
        ):
            print("Update from intelligent.think", r.choices[0].message.parsed)
            self.context.update(r.choices[0].message.parsed)
            if r.choices[0].message.tool_calls is not None:
                return await self.process(r)

    async def process(self, res=None):
        if r := (
            await Providers.openai.beta.chat.completions.create(**config(self.model))
            if res is None
            else res
        ):
            if tc := r.choices[0].message.tool_calls:
                if c := await getattr(self, tc.function.name)(
                    **json.loads(tc.function.arguments)
                ):
                    self.context.update(
                        ToolCall(
                            tc.id,
                            tc.function.name,
                            json.loads(tc.function.arguments),
                        )
                    )
                    c.tool_call_id = tc.id
                    return await self.think()

    def classify(input: str):
        return (
            Providers.openai_sync.embeddings.create(
                **{"model": "text-embedding-3-small", "input": str(input)}
            )
            .data[0]
            .embedding
        )
