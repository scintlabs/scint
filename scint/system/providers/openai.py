import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential
from scint.services.logging import logger
from scint.system.config import envar

api_key = envar("OPENAI_API_KEY")

if api_key is None:
    logger.error("The environment variable 'OPENAI_API_KEY' is not set.")
    raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")


async def function_call(functions):
    data = await openai.ChatCompletion.acreate(functions=functions)
    return data


async def chat(**kwargs):
    response = await openai.ChatCompletion.acreate(
        model=kwargs.get("model"),
        max_tokens=kwargs.get("max_tokens", 4096),
        presence_penalty=kwargs.get("presence_penalty", 0.3),
        frequency_penalty=kwargs.get("frequency_penalty", 0.3),
        top_p=kwargs.get("top_p", 0.5),
        temperature=kwargs.get("temperature", 1.8),
        messages=kwargs.get("messages"),
        # functions=kwargs.get("functions"),
        # function_call=kwargs.get("function_call", "auto"),
        user=kwargs.get("user"),
    )
    return response


async def chat_completion(messages):
    logger.info(f"Sending message object to the API.")
    data = await openai.ChatCompletion.acreate(
        model="gpt-4-0613",
        temperature=1.7,
        top_p=0.5,
        n=1,
        stop=[],
        max_tokens=4096,
        presence_penalty=0.35,
        frequency_penalty=0.35,
        messages=messages,
        user="ScintDiscord",
    )

    return data


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str) -> list[float]:
    model = "text-embedding-ada-002"
    return openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]  # type: ignore
