import asyncio, json, logging, subprocess
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import List
from core.data.providers import openai_chat
from core.prompt import Prompt, meta
import subprocess


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def complete(message: str, prompt: List[Prompt]) -> str:  # type: ignore
    """"""
    messages = []
    messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": message})
    response = await openai_chat(messages)

    if response is None:
        raise ValueError("Error.")

    message = response["choices"][0]["message"].get("content")
    return message
