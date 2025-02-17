from __future__ import annotations
import json

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from scint.api.types import Aspect, Struct
from scint.api.models import Message, Response, FunctionCall

openai_client: AsyncOpenAI = AsyncOpenAI()
anthropic_client: AsyncAnthropic = AsyncAnthropic()


class Intelligence(Aspect):
    async def parse_message(struct: Struct):
        req = {
            "model": "gpt-4o",
            "temperature": 1.4,
            "top_p": 0.6,
            "response_format": Response,
            **struct.model,
        }

        data = []
        res = await openai_client.beta.chat.completions.parse(**req)

        if res.choices[0].message.parsed:
            data.append(res.choices[0].message.parsed)

        if res.choices[0].message.tool_calls:
            data.append(res.choices[0].message)
            for call in res.choices[0].message.tool_calls:
                data.append(
                    FunctionCall(
                        id=call.id,
                        name=call.function.name,
                        arguments=json.loads(call.function.arguments),
                    )
                )
        for d in data:
            return d

    async def parse_image(context):
        pass

    async def generate_tool_call(context):
        req = {
            "model": "gpt-4o",
            "temperature": 1.2,
            "top_p": 0.8,
            "tool_choice": "required",
            **context.model,
        }
        res = await openai_client.chat.completions.create(**req)
        return res.choices[0].message.parsed

    async def generate_image(context):
        req = {"quality": "hd", "size": "1024x1024", "n": 1, "style": "vibrant"}
        res = await openai_client.images.generate.create(**req)
        return res.choices[0].data.url

    async def generate_embedding(message: Message):
        req = {
            "model": "text-embedding-3-small",
            "input": "".join([b.data for b in message.content]),
        }
        res = await openai_client.embeddings.create(**req)
        message.embedding = res.data[0].embedding
        return message
