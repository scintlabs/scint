from __future__ import annotations

from enum import Enum
from typing import Any

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from src.core.types import Aspect

opai = AsyncOpenAI()
anth = AsyncAnthropic()


class IntelligencePreset(Enum):
    completion = {
        "model": "gpt-4o",
        "temperature": 1.4,
        "top_p": 0.6,
        # "response_format": AssistantMessage,
    }
    image = {"quality": "hd", "size": "1024x1024", "n": 1, "style": "vibrant"}
    vector = {"model": "text-embedding-3-small"}


class Agentic(Aspect):
    async def input(self, data: Any):
        self.context.update(data)
        return await self.parse(data)

    async def parse(self, data: Any):
        res = await self.generate(self.context)
        return await self.output(res)

    async def output(self, data: Any):
        self.context.update(data)
        return data

    async def generate(self, context):
        req = {**context.model, **IntelligencePreset["completion"].value}
        res = await opai.beta.chat.completions.parse(**req)
        return res.choices[0].message.parsed

    async def embed(self, input: str):
        req = {"model": "text-embedding-3-small", "input": input}
        res = await opai.embeddings.create(**req)
        return res.data[0].embedding

    async def classify(self, message):
        req = {
            "messages": [
                [
                    {
                        "role": "system",
                        "content": "Provide a succint description of the following message and select the most appropriate interface for responding to it.",
                    }
                ],
                {"role": "user", "content": str(message.string)},
            ],
            "model": "gpt-4o-mini",
            "response_format": None,
        }
        return await opai.beta.chat.completions.parse(**req)

    @property
    def model(self):
        return {
            "messages": [i.model for i in self.prompts if self.prompts]
            + [m.model for m in self.messages],
            "functions": [f.model for f in self.functions],
        }
