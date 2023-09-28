from typing import List
from openai import ChatCompletion
from base.observability.logging import logger

from base.persistence.env import envar
from base.providers import OpenAIMessage
from base.processing.functions import OpenAIFunction
from config import user

api_key = envar("OPENAI_API_KEY")

if api_key is None:
    logger.error("This action requires an OpenAI API key.")
    raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")


async def chat_completion(messages, functions):
    data = await ChatCompletion.acreate(
        model="gpt-4-0613",
        temperature=1.7,
        top_p=0.5,
        n=1,
        stop=[],
        max_tokens=4096,
        presence_penalty=0.35,
        frequency_penalty=0.35,
        logit_bias=user.logit_bias,
        messages=messages,
        functions=functions,
        function_call="auto",
        stream=False,
        user="Tim",
    )

    return data
