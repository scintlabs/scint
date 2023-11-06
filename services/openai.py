import json
from typing import List

import openai

from services.logger import log
from core.config import GPT4


def count_tokens(prompt_tokens, completion_tokens):
    log.info(f"Token usage: {prompt_tokens} prompt, {completion_tokens} completion.")
    # TODO: Calculate token usage


async def summary(**kwargs):
    log.info(f"OpenAI Service: sending request to language model.")

    parameters = {
        "model": kwargs.get("model", GPT4),
        "temperature": kwargs.get("temperature", 1.5),
        "top_p": kwargs.get("top_p", 0.5),
        "presence_penalty": kwargs.get("presence_penalty", 0.3),
        "frequency_penalty": kwargs.get("frequency_penalty", 0.3),
        "messages": kwargs.get("messages"),
    }

    if kwargs.get("functions"):
        parameters["functions"] = kwargs.get("functions")
        parameters["function_call"] = kwargs.get("function_call", "auto")

    response = await openai.ChatCompletion.acreate(**parameters)
    response_message = response["choices"][0].get("message")
    prompt_tokens = response["usage"].get("prompt_tokens")
    completion_tokens = response["usage"].get("completion_tokens")
    count_tokens(prompt_tokens, completion_tokens)

    log.info(f"OpenAI Service: response received from language model.")

    return response_message


async def completion(**kwargs):
    log.info(f"OpenAI Service: sending request to language model.")

    parameters = {
        "model": kwargs.get("model", GPT4),
        "max_tokens": kwargs.get("max_tokens", 4096),
        "temperature": kwargs.get("temperature", 1),
        "top_p": kwargs.get("top_p", 1),
        "presence_penalty": kwargs.get("presence_penalty", 0.3),
        "frequency_penalty": kwargs.get("frequency_penalty", 0.3),
        "messages": kwargs.get("messages"),
    }

    if kwargs.get("functions"):
        parameters["functions"] = kwargs.get("functions")
        parameters["function_call"] = kwargs.get("function_call", "auto")

    response = await openai.ChatCompletion.acreate(**parameters)
    response_message = response["choices"][0].get("message")
    prompt_tokens = response["usage"].get("prompt_tokens")
    completion_tokens = response["usage"].get("completion_tokens")
    count_tokens(prompt_tokens, completion_tokens)

    log.info(f"OpenAI Service: response received from language model.")

    return response_message


async def embedding(text: str) -> List[float]:
    log.info(f"Sending embedding request to language model.")

    model = "text-embedding-ada-002"
    response = await openai.Embedding.acreate(input=[text], model=model)
    log.info(f"Response received from language model.")

    return response["data"][0]["embedding"]  # type: ignore
