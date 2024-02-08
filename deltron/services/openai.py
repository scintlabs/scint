from typing import Any, Dict, List

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from deltron.constants import GPT3, GPT4_TURBO
from deltron.utils.logger import log

openai_async = AsyncOpenAI()
openai_completions = openai_async.chat.completions
openai_embeddings = openai_async.embeddings


class Config:
    def __init__(self, config: Dict[str, Any]):
        self.model: str = config.get("model")
        self.top_p: float = config.get("top_p")
        self.temperature: float = config.get("temperature")
        self.presence_penalty: float = config.get("presence_penalty")
        self.frequency_penalty: float = config.get("frequency_penalty")

    def metadata(self) -> Dict[str, any]:
        return {
            "model": self.model,
            "top_p": self.top_p,
            "temperature": self.temperature,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
        }


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(max_attempt_number=3))
async def completion(**kwargs):
    log.info(kwargs)
    parameters = {
        "model": GPT4_TURBO,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0.35,
        "frequency_penalty": 0.35,
        "messages": kwargs.get("messages"),
        "tools": kwargs.get("tools"),
        "tool_choice": kwargs.get("tool_choice", "auto"),
    }

    try:
        response = await openai_completions.create(**parameters)
        response = response.model_dump()
        message = response["choices"][0].get("message")
        tool_calls = message.get("tool_calls")

        if tool_calls is not None:
            yield tool_calls

        else:
            log.info("The model didn't return a tool call.")
            yield

    except Exception as e:
        log.info(f"{e}")


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
async def x(**kwargs):
    parameters = {
        "model": GPT4_TURBO,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0.35,
        "frequency_penalty": 0.35,
        "messages": kwargs.get("messages"),
        "tools": kwargs.get("tools"),
        "tool_choice": kwargs.get("tool_choice", "auto"),
    }

    response = await openai_completions.create(**parameters)
    response = response.model_dump()
    response_message = response["choices"][0].get("message")
    tool_calls = response_message.get("tool_calls")

    async for tool_call in tool_calls:
        yield tool_call


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
