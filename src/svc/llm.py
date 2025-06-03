from __future__ import annotations

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI, OpenAI

from src.svc.utils import env


ANTHROPIC_API_KEY = env("OPENAI_API_KEY")
ANTHROPIC_CLIENT = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
OPENAI_API_KEY = env("OPENAI_API_KEY")
OPENAI_CLIENT = AsyncOpenAI(api_key=OPENAI_API_KEY)
OPENAI_CLIENT_S = OpenAI(api_key=OPENAI_API_KEY)


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
