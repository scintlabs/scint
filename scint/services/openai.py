import json
from typing import List

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from scint.conf import GPT3, GPT4_TURBO
from scint.services.logger import log

openai_async = AsyncOpenAI()
openai_completions = openai_async.chat.completions
openai_embeddings = openai_async.embeddings


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
async def tool_completion(**process_state):
    response = await openai_completions.create(**process_state)
    response = response.model_dump()
    response_message = response["choices"][0].get("message")
    tool_calls = response_message.get("tool_calls")

    try:
        async for completions in tool_completion(**process_state):
            for tool_call in completions:
                function = tool_call.get("function")
                tool_name = function.get("name")
                func_args = json.loads(function.get("arguments", "{}"))
                tool_instance = process_state.tools.get(tool_name)

                try:
                    if tool_instance is not None:
                        response = await tool_instance.execute_action(**func_args)
                        log.info(response.data_dump())
                        yield response

                except Exception as e:
                    log.info(f"OpenAI Service: {e}")
                    raise

    except Exception as e:
        log.info(f"OpenAI Service: {e}")
        raise

    if tool_calls is not None:
        yield tool_calls


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
async def message_completion(**kwargs):
    log.info(f"OpenAI Service: sending completion request.")

    parameters = {
        "model": kwargs.get("model", GPT4_TURBO),
        "temperature": kwargs.get("temperature", 1),
        "top_p": kwargs.get("top_p", 1),
        "presence_penalty": kwargs.get("presence_penalty", 0.35),
        "frequency_penalty": kwargs.get("frequency_penalty", 0.35),
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
async def get_summary(content: str) -> str:
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
async def get_embedding(text: str) -> List[float]:
    log.info(f"OpenAI Service: sending embedding request.")

    model = "text-embedding-ada-002"

    try:
        response = await openai_embeddings.create(input=[text], model=model)
        log.info(f"OpenAI Service: embedding received from language model.")

        return response["data"][0]["embedding"]

    except Exception as e:
        log.info(f"OpenAI Service: there was an exception: {e}")
        raise
