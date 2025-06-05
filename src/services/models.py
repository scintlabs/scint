from __future__ import annotations
import random

from attrs import define, field


from src.services.utils import env


async def _stream(res):
    async for part in res:
        yield part


async def response(req):
    return await OPENAI_CLIENT.responses.create(**req)


async def completion(req):
    OPENAI_CLIENT.chat.completions.create(**req)


async def embedding(input: str):
    req = {"model": "text-embedding-3-small", "input": str(input)}
    res = await OPENAI_CLIENT.embeddings.create(**req)
    return res.data[0].embedding


async def image():
    req = {"quality": "hd", "size": "1024x1024", "n": 1, "style": "vibrant"}
    res = await OPENAI_CLIENT.images.generate.create(**req)
    return res.choices[0].library.url


@define
class ModelConfig:
    model: str = field(default="gpt-4.1")
    top_p: float = field(default=round(random.uniform(0.5, 1), 2))
    temperature: float = field(default=round(random.uniform(0.9, 1.7), 2))
