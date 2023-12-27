import json
from typing import List

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from scint.config import GPT3, GPT4_TURBO
from scint.services.logger import log

openai_async = AsyncOpenAI()
openai_completions = openai_async.chat.completions
openai_embeddings = openai_async.embeddings


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
async def completion(**kwargs):
    log.info(f"OpenAI Service: sending completion request.")
    # log.info(kwargs)

    parameters = {
        "model": kwargs.get("model", GPT4_TURBO),
        "max_tokens": kwargs.get("max_tokens", 8192),
        "temperature": kwargs.get("temperature", 1),
        "top_p": kwargs.get("top_p", 1),
        "presence_penalty": kwargs.get("presence_penalty", 0.3),
        "frequency_penalty": kwargs.get("frequency_penalty", 0.3),
        "messages": kwargs.get("messages"),
    }

    if kwargs.get("tools") is not None:
        parameters["tools"] = kwargs.get("tools")
        parameters["tool_choice"] = kwargs.get("tool_choice", "auto")

    try:
        response = await openai_completions.create(**parameters)
        response = response.model_dump()
        response_message = response["choices"][0].get("message")

        log.info(f"OpenAI Service: completion received from language model.")

        return response_message

    except Exception as e:
        log.info(f"OpenAI Service: there was an exception: {e}")
        raise


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
async def classification(**kwargs):
    log.info(f"OpenAI Service: sending classification request.")

    parameters = {
        "model": kwargs.get("model", GPT4_TURBO),
        "max_tokens": kwargs.get("max_tokens", 4096),
        "temperature": kwargs.get("temperature", 1),
        "top_p": kwargs.get("top_p", 1),
        "presence_penalty": kwargs.get("presence_penalty", 0.3),
        "frequency_penalty": kwargs.get("frequency_penalty", 0.3),
        "messages": kwargs.get("messages"),
        "tools": kwargs.get("tools"),
        "tool_choice": kwargs.get("tool_choice", "auto"),
    }
    try:
        response = await openai_completions.create(**parameters)
        response = response.model_dump()
        response_message = response["choices"][0].get("message")
        tool_calls = response_message.get("tool_calls")

        if tool_calls is not None:
            log.info(f"OpenAI Service: classification received from language model.")

            for tool_call in tool_calls:
                function = tool_call.get("function")
                function_name = function.get("name")

                if function_name == "classifier":
                    function_args = json.loads(function.get("arguments"))
                    request_type = function_args.get("request_type")
                    keyword = function_args.get("keyword")
                    named_entities = function_args.get("named_entities")

                    return request_type, keyword, named_entities

    except Exception as e:
        log.info(f"OpenAI Service: there was an exception during classification: {e}")
        raise


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
async def summary(content: str) -> str:
    log.info(f"OpenAI Service: sending summary request.")

    parameters = {
        "model": GPT3,
        "temperature": 0.8,
        "top_p": 0.4,
        "presence_penalty": 0.4,
        "frequency_penalty": 0.4,
        "messages": [
            {
                "role": "system",
                "content": "You are a compression algorithm. Summarize content.",
            },
            {
                "role": "system",
                "content": content,
            },
        ],
    }

    try:
        response = await openai_completions.create(**parameters)
        response = response.model_dump()
        summarized_content = response["choices"][0]["message"].get("content")
        log.info(f"OpenAI Service: summary received from language model.")

        return summarized_content

    except Exception as e:
        log.info(f"OpenAI Service: there was an exception: {e}")
        raise


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
async def embedding(text: str) -> List[float]:
    log.info(f"OpenAI Service: sending embedding request.")

    model = "text-embedding-ada-002"

    try:
        response = await openai_embeddings.create(input=[text], model=model)
        log.info(f"OpenAI Service: embedding received from language model.")

        return response["data"][0]["embedding"]

    except Exception as e:
        log.info(f"OpenAI Service: there was an exception: {e}")
        raise
