from typing import List

import openai


from services.logger import log


async def completion(**kwargs):
    log.info(f"Sending completion request to language model.")

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

    log.info(f"Response received from language model.")
    return response["choices"][0].get("message")


async def embedding(text: str) -> List[float]:
    log.info(f"Sending embedding request to language model.")

    model = "text-embedding-ada-002"
    response = await openai.Embedding.acreate(input=[text], model=model)

    log.info(f"Response received from language model.")
    return response["data"][0]["embedding"]  # type: ignore
