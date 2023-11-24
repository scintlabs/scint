from typing import List

from openai import OpenAI, AsyncOpenAI
from tenacity import wait_random_exponential, stop_after_attempt, retry

from services.logger import log
from core.config import GPT4, GPT3


openai_sync = OpenAI()
openai_async = AsyncOpenAI()
openai_assistants = openai_sync.beta.assistants
openai_threads = openai_sync.beta.threads
openai_files = openai_sync.files
openai_completions = openai_async.chat.completions
openai_embeddings = openai_async.embeddings


def count_tokens(prompt_tokens, completion_tokens):
    log.info(f"Token usage: {prompt_tokens} prompt, {completion_tokens} completion.")
    # TODO: Calculate token usage


async def summary(**kwargs):
    log.info(f"OpenAI Service: sending summary request.")

    parameters = {
        "model": kwargs.get("model", GPT3),
        "temperature": kwargs.get("temperature", 1),
        "top_p": kwargs.get("top_p", 1),
        "presence_penalty": kwargs.get("presence_penalty", 0.5),
        "frequency_penalty": kwargs.get("frequency_penalty", 0.5),
        "messages": kwargs.get("messages"),
    }

    response = await openai_completions.create(**parameters)
    response = response.model_dump()
    response_message = response["choices"][0].get("message")
    log.info(f"OpenAI Service: summary received from language model.")

    return response_message


async def completion(**kwargs):
    log.info(f"OpenAI Service: sending completion request.")

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
        parameters["function_call"] = kwargs.get("function_call")

    try:
        response = await openai_completions.create(**parameters)
        log.info(response)
        response = response.model_dump()
        response_message = response["choices"][0].get("message")
        log.info(f"OpenAI Service: completion received from language model.")

        return response_message

    except Exception:
        log.info(response_message)
        log.info(f"OpenAI Service: there was an exception.")


async def embedding(text: str) -> List[float]:
    log.info(f"OpenAI Service: sending embedding request.")

    model = "text-embedding-ada-002"
    response = await openai_embeddings.create(input=[text], model=model)
    log.info(f"OpenAI Service: embedding received from language model.")

    return response["data"][0]["embedding"]  # type: ignore
