import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential

from services.logger import log


async def completion(**kwargs):
    log.info(f"Sending request to language model: {kwargs}")

    response = await openai.ChatCompletion.acreate(
        model=kwargs.get("model"),
        max_tokens=kwargs.get("max_tokens", 4096),
        presence_penalty=kwargs.get("presence_penalty", 0.3),
        frequency_penalty=kwargs.get("frequency_penalty", 0.3),
        top_p=kwargs.get("top_p", 0.7),
        temperature=kwargs.get("temperature", 1.9),
        messages=kwargs.get("messages"),
        functions=kwargs.get("functions"),
        function_call=kwargs.get("function_call", "auto"),
    )

    log.info(f"Response received from language model: {response}")
    return response


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
async def get_embedding(text: str) -> list[float]:
    model = "text-embedding-ada-002"
    return openai.Embedding.acreate(input=[text], model=model)["data"][0]["embedding"]  # type: ignore
