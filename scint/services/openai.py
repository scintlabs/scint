from typing import List

from core.config import GPT3, GPT4
from openai import AsyncOpenAI
from services.logger import log
from tenacity import retry, stop_after_attempt, wait_random_exponential

openai_async = AsyncOpenAI()
openai_completions = openai_async.chat.completions
openai_embeddings = openai_async.embeddings


def count_tokens(prompt_tokens, completion_tokens):
    log.info(f"Token usage: {prompt_tokens} prompt, {completion_tokens} completion.")
    # TODO: Calculate token usage


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
async def generate_completion(**kwargs):
    log.info(f"OpenAI Service: sending completion request.")

    parameters = {
        "model": kwargs.get("model", GPT4),
        "max_tokens": kwargs.get("max_tokens", 4096),
        "temperature": kwargs.get("temperature", 1),
        "top_p": kwargs.get("top_p", 1),
        "presence_penalty": kwargs.get("presence_penalty", 0.3),
        "frequency_penalty": kwargs.get("frequency_penalty", 0.3),
        "messages": kwargs.get("messages"),
        "functions": kwargs.get("functions"),
    }

    log.info(parameters)

    try:
        response = await openai_completions.create(**parameters)
        response = response.model_dump()
        response_message = response["choices"][0].get("message")
        log.info(f"OpenAI Service: completion received from language model.")

        return response_message

    except Exception as e:
        log.info(f"OpenAI Service: there was an exception: {e}")
        raise


async def generate_summary(content: str) -> str:
    log.info(f"OpenAI Service: sending summary request.")

    parameters = {
        "model": GPT3,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0.5,
        "frequency_penalty": 0.5,
        "messages": [
            {
                "role": "system",
                "content": "You are a compression algorithm. For every message, summarize content using shorthand language. Maintan original author's perspective.",
            },
            {"role": "system", "content": content},
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


async def generate_embedding(text: str) -> List[float]:
    log.info(f"OpenAI Service: sending embedding request.")

    model = "text-embedding-ada-002"
    response = await openai_embeddings.create(input=[text], model=model)
    log.info(f"OpenAI Service: embedding received from language model.")

    return response["data"][0]["embedding"]
