from typing import Any, Dict, List

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from scint.constants import GPT4_TURBO
from scint.utils.logger import log

openai_async = AsyncOpenAI()
openai_completions = openai_async.chat.completions
openai_embeddings = openai_async.embeddings

tenacity_wait = wait_random_exponential(min=1, max=40)
tenacity_stop = stop_after_attempt(max_attempt_number=3)


def get_parameters(**params) -> Dict[str, Any]:
    parameters = {
        "model": params.get("model", GPT4_TURBO),
        "temperature": params.get("temperature", 1),
        "top_p": params.get("top_p", 1),
        "presence_penalty": params.get("presence_penalty", 0),
        "frequency_penalty": params.get("frequency_penalty", 0),
        "messages": params.get("messages", []),
        "tools": params.get("tools", []),
        "tool_choice": params.get("tool_choice", "auto"),
    }

    return parameters


@retry(wait=tenacity_wait, stop=tenacity_stop)
async def chat_completion(**params):
    try:
        response = await openai_completions.create(**params)
        response = response.model_dump()
        message = response["choices"][0].get("message")
        if message is not None:
            content = message.get("content")
            yield content

        else:
            log.info("The model didn't return a completion.")
            yield

    except Exception as e:
        log.info(f"{e}")


@retry(wait=tenacity_wait, stop=tenacity_stop)
async def tool_completion(**params):
    try:
        parameters = get_parameters(**params)
        response = await openai_completions.create(**parameters)
        response = response.model_dump()
        message = response["choices"][0].get("message")
        if message is not None:
            tool_calls = message.get("tool_calls")
            yield tool_calls

        else:
            log.info("The model didn't return a tool call.")
            yield

    except Exception as e:
        log.info(f"{e}")


@retry(wait=tenacity_wait, stop=tenacity_stop)
async def embedding(**params):
    try:
        embedding = None
        parameters = get_parameters(**params)
        response = await openai_embeddings.create(**parameters)
        if response is not None:
            response_dump = response.model_dump()
            embedding = response_dump["data"][0]["embedding"]

        if embedding is not None:
            yield embedding

        yield
    except Exception as e:
        log.info(e)
        raise
