import asyncio, os, openai
from typing import List, Dict, Any
from core.util import minify


async def openai_chat(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    openai.api_key = os.environ["OPENAI_API_KEY"]
    logit_bias = {1102: -100, 4717: -100, 7664: -100}

    if openai.api_key is None:
        raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")

    response = await openai.ChatCompletion.acreate(
        model="gpt-4-0613",
        temperature=1.6,
        top_p=0.8,
        frequency_penalty=0.35,
        presence_penalty=0.35,
        logit_bias=logit_bias,
        messages=messages,
    )
    return response  # type: ignore
