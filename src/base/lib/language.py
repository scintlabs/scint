from enum import Enum

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from ..models import InputMessage, OutputMessage


opai = AsyncOpenAI()
anth = AsyncAnthropic()


class Presets(Enum):
    text = {
        "model": "gpt-4o",
        "temperature": 1.4,
        "top_p": 0.6,
        "response_format": OutputMessage,
    }
    image = {"quality": "hd", "size": "1024x1024", "n": 1, "style": "vibrant"}
    vector = {"model": "text-embeddings-3-small"}


async def get_completion(context):
    req = context.schema
    req.update(Presets.text.value)
    res = await opai.beta.chat.completions.parse(**req)
    return res.choices[0].message.parsed


async def get_embedding(message: InputMessage):
    res = await opai.embeddings.create(
        input=[b.data for b in message.content], model="text-embeddings-3-small"
    )
    message.embedding = res.data[0].embedding
    return message


__all__ = Presets, get_completion, get_embedding
