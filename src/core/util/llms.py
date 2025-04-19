from __future__ import annotations

import random
from typing import Any, Literal

from openai import AsyncOpenAI, OpenAI

from src.core.util.transforms import transform


oai = AsyncOpenAI()
oai_sync = OpenAI()


def build_request(input, protocol):
    instructions, output, tools = protocol()
    return {
        "instructions": instructions["content"],
        "input": input.content,
        "text": {"format": transform(output)},
        "tools": [t.schema for t in tools],
        "model": "gpt-4.1",
        "top_p": round(random.uniform(0.5, 1), 2),
        "temperature": round(random.uniform(0.9, 1.7), 2),
        "store": False,
    }


def generate_desc(obj: Any, kind: Literal["function", "session", "object"]):
    req = {
        "model": "gpt-4.1",
        "top_p": round(random.uniform(0.5, 1), 2),
        "temperature": round(random.uniform(0.9, 1.7), 2),
        "store": False,
    }
    msg = None
    if kind == "function":
        msg = "Generate a description for this function, which is used in the `description` field when serializing it. Avoid describing implementation details and simply provide a general description of the object and what it's used for in one or two sentences:"
    elif kind == "session":
        msg = "Generate a name and description for this conversation, which is used to populate the class object's `name` and `description` fields. Simple provide a concise name in the form of a title and a one-sentence description. Return the name on the first line and the description on the second line."

    req["input"] = f"{msg}\n\n{obj}"
    res = oai_sync.responses.create(**req)
    if res.output_text is not None:
        return res.output_text


def embedding(input: str):
    req = {"model": "text-embedding-3-small", "input": str(input)}
    res = oai_sync.embeddings.create(**req)
    return res.data[0].embedding


async def tool_call():
    req = {
        "model": "gpt-4.1",
        "top_p": round(random.uniform(0.5, 1), 2),
        "temperature": round(random.uniform(0.9, 1.7), 2),
        "store": False,
        "tool_choice": "required",
    }
    res = await oai.chat.completions.create(**req)
    return res.choices[0].message.parsed


async def image():
    req = {"quality": "hd", "size": "1024x1024", "n": 1, "style": "vibrant"}
    res = await oai.images.generate.create(**req)
    return res.choices[0].library.url
